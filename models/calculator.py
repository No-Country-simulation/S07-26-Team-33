"""
Motor de cálculo principal
CORREGIDO: 
- CapEx ya no se trata como pérdida anual
- Se agregó Costo de Oportunidad del Capital
- Se agregaron rangos de confianza
- Todas las unidades son dimensionalmente consistentes
"""

import numpy as np
from .lookup_tables import (
    get_clima, get_pue, get_peak_delta, 
    get_safety_margin, get_benchmark, get_growth_rate
)
from .datasets import (
    get_tarifa_by_country, get_capex_by_country_tier,
    get_revenue_by_country_tier
)

# ============================================
# CONSTANTES
# ============================================

HORAS_ANUALES = 8760
HORIZONTE_AMORTIZACION = 10  # años

# ============================================
# SUPUESTOS CLAVE DEL MODELO (DOCUMENTADOS)
# ============================================

# Fuente: Uptime Institute (2024) - Factor de energización típico en data centers
FACTOR_ENERGIZADO = 0.70  # 70% de la capacidad stranded está realmente energizada

# Fuente: Deloitte Data Center Investment Report (2024)
# WACC (Costo de Capital) típico para inversiones en data centers
COSTO_OPORTUNIDAD_CAPITAL = 0.10  # 10% anual

# Fuente: AFCOM Industry Survey (2024)
# Porcentaje de capacidad stranded que puede ser recuperada
FACTOR_RECUPERACION = 0.60  # 60% es recuperable en el mejor caso

# Incertidumbre estándar por variable (basado en variabilidad de datos públicos)
INCERTIDUMBRE = {
    'stranded_mw': 0.12,        # ±12%
    'energy_loss': 0.15,        # ±15%
    'stranded_capex': 0.10,     # ±10%
    'costo_oportunidad': 0.15,  # ±15%
    'perdida_total': 0.18,      # ±18%
    'recovery_time': 0.20,      # ±20%
}


# ============================================
# FUNCIÓN DE RANGOS
# ============================================

def calcular_rangos(valor_central, incertidumbre_pct):
    """
    Calcula rangos de confianza basados en incertidumbre de inputs
    
    Args:
        valor_central: valor estimado
        incertidumbre_pct: porcentaje de incertidumbre (0-1)
    
    Returns:
        dict: {'central': x, 'inferior': y, 'superior': z, 'rango_pct': p}
    """
    rango_inferior = valor_central * (1 - incertidumbre_pct)
    rango_superior = valor_central * (1 + incertidumbre_pct)
    
    # Asegurar que no sean negativos
    rango_inferior = max(0, rango_inferior)
    rango_superior = max(0, rango_superior)
    
    return {
        'central': valor_central,
        'inferior': rango_inferior,
        'superior': rango_superior,
        'rango_pct': incertidumbre_pct * 100
    }


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def calcular_todo(facility_mw, avg_util_pct, cooling_type, pais, tier, market_demand):
    """
    Calcula todos los resultados del modelo
    
    Args:
        facility_mw: Capacidad total en MW
        avg_util_pct: Utilización promedio (0-100)
        cooling_type: 'Air-cooled', 'Liquid-cooled', 'Hybrid'
        pais: Nombre del país
        tier: 'Tier I', 'Tier II', 'Tier III', 'Tier IV'
        market_demand: 'Baja', 'Media', 'Alta', 'Muy Alta'
    
    Returns:
        dict: Todos los resultados calculados
    """
    
    # Convertir a decimal
    avg_util = avg_util_pct / 100
    
    # ============================================
    # 1. OBTENER PARÁMETROS
    # ============================================
    
    clima = get_clima(pais)
    pue = get_pue(cooling_type, clima)
    tarifa = get_tarifa_by_country(pais)
    capex_per_mw = get_capex_by_country_tier(pais, tier)
    revenue_per_mw = get_revenue_by_country_tier(pais, tier)
    peak_delta = get_peak_delta(tier)
    safety_margin = get_safety_margin(tier)
    benchmark = get_benchmark(tier)
    growth_rate = get_growth_rate(market_demand)
    
    # ============================================
    # 2. CÁLCULOS DE CAPACIDAD
    # ============================================
    
    # Capacidad ociosa
    idle_pct = 1 - avg_util
    idle_mw = facility_mw * idle_pct
    
    # Utilización pico
    peak_util = avg_util + peak_delta
    peak_util_pct = peak_util * 100
    
    # Headroom requerido
    headroom_pct = 1 - peak_util - safety_margin
    headroom_pct = max(0, headroom_pct)  # No negativo
    
    # Stranded Capacity (NO puede ser negativo)
    stranded_pct = max(0, idle_pct - headroom_pct)
    stranded_mw = facility_mw * stranded_pct
    
    # Capacidad efectiva
    effective_capacity = facility_mw * avg_util
    
    # ============================================
    # 3. CÁLCULOS ECONÓMICOS - CORREGIDOS
    # ============================================
    
    # 3.1 Pérdida energética anual (SÍ es anual)
    # Solo la capacidad stranded que está realmente energizada consume energía
    stranded_mw_energizado = stranded_mw * FACTOR_ENERGIZADO
    
    energy_loss = stranded_mw_energizado * HORAS_ANUALES * pue * tarifa
    
    # 3.2 Capital inmovilizado en capacidad stranded (NO es anual, es valor total)
    stranded_capex = stranded_mw * capex_per_mw
    
    # 3.3 Costo de oportunidad del capital (anualizado)
    # Representa lo que podría ganar ese capital si se invirtiera en otra cosa
    costo_oportunidad_anual = stranded_capex * COSTO_OPORTUNIDAD_CAPITAL
    
    # 3.4 Pérdida total anual (energía + costo de oportunidad)
    # AHORA SÍ son dimensionalmente consistentes: $/año + $/año
    perdida_anual_total = energy_loss + costo_oportunidad_anual
    
    # 3.5 Pérdida por MW (anual)
    loss_per_mw = perdida_anual_total / stranded_mw if stranded_mw > 0 else 0
    
    # ============================================
    # 4. VALOR RECUPERABLE
    # ============================================
    
    if revenue_per_mw > 0:
        # Solo un % de la capacidad stranded es realmente recuperable
        stranded_mw_recuperable = stranded_mw * FACTOR_RECUPERACION
        
        # Ingreso potencial anual
        revenue_potential_anual = stranded_mw_recuperable * revenue_per_mw
        
        # Costos evitados al recuperar (energía + oportunidad)
        costs_avoided_anual = (energy_loss * 0.5) + (costo_oportunidad_anual * 0.3)
        
        # Valor recuperable anual
        recoverable_value = revenue_potential_anual - costs_avoided_anual
        recoverable_value = max(0, recoverable_value)  # No negativo
    else:
        recoverable_value = 0
        revenue_potential_anual = 0
        costs_avoided_anual = 0
    
    # ============================================
    # 5. TIEMPO DE RECUPERACIÓN
    # ============================================
    
    if stranded_pct > 0 and growth_rate > 0:
        target_util = min(avg_util + stranded_pct, 0.95)  # Máximo 95%
        recovery_time = np.log(target_util / avg_util) / np.log(1 + growth_rate)
        recovery_time = max(0, recovery_time)  # No negativo
    else:
        recovery_time = 0
        target_util = avg_util
    
    # ============================================
    # 6. INDICADORES
    # ============================================
    
    utilization_gap = (avg_util - benchmark) * 100  # en puntos porcentuales
    
    # Escenarios de recuperación
    if recovery_time > 0:
        recovery_optimista = np.log(target_util / avg_util) / np.log(1 + growth_rate * 1.15)
        recovery_pesimista = np.log(target_util / avg_util) / np.log(1 + growth_rate * 0.85)
    else:
        recovery_optimista = 0
        recovery_pesimista = 0
    
    # ============================================
    # 7. GENERAR RANGOS PARA CADA OUTPUT
    # ============================================
    
    rangos = {
        'stranded_mw': calcular_rangos(stranded_mw, INCERTIDUMBRE['stranded_mw']),
        'energy_loss': calcular_rangos(energy_loss, INCERTIDUMBRE['energy_loss']),
        'stranded_capex': calcular_rangos(stranded_capex, INCERTIDUMBRE['stranded_capex']),
        'costo_oportunidad_anual': calcular_rangos(costo_oportunidad_anual, INCERTIDUMBRE['costo_oportunidad']),
        'perdida_anual_total': calcular_rangos(perdida_anual_total, INCERTIDUMBRE['perdida_total']),
        'recovery_time': calcular_rangos(recovery_time, INCERTIDUMBRE['recovery_time']),
        'recoverable_value': calcular_rangos(recoverable_value, 0.25),
    }
    
    # ============================================
    # 8. RESULTADOS
    # ============================================
    
    return {
        # Parámetros usados
        'clima': clima,
        'pue': pue,
        'tarifa': tarifa,
        'capex_per_mw': capex_per_mw,
        'revenue_per_mw': revenue_per_mw,
        'peak_delta': peak_delta,
        'safety_margin': safety_margin,
        'benchmark': benchmark,
        'growth_rate': growth_rate,
        
        # Supuestos del modelo (para transparencia)
        'factor_energizado': FACTOR_ENERGIZADO,
        'costo_oportunidad': COSTO_OPORTUNIDAD_CAPITAL,
        'factor_recuperacion': FACTOR_RECUPERACION,
        
        # Capacidad
        'facility_mw': facility_mw,
        'avg_util_pct': avg_util_pct,
        'avg_util': avg_util,
        'idle_pct': idle_pct * 100,
        'idle_mw': idle_mw,
        'peak_util_pct': peak_util_pct,
        'headroom_pct': headroom_pct * 100,
        'stranded_pct': stranded_pct * 100,
        'stranded_mw': stranded_mw,
        'effective_capacity': effective_capacity,
        
        # Económico (CORREGIDO)
        'energy_loss': energy_loss,                      # $/año
        'stranded_capex': stranded_capex,                # $ (capital inmovilizado)
        'costo_oportunidad_anual': costo_oportunidad_anual,  # $/año
        'perdida_anual_total': perdida_anual_total,      # $/año (ENERGÍA + OPORTUNIDAD)
        'loss_per_mw': loss_per_mw,                      # $/año por MW
        'recoverable_value': recoverable_value,          # $/año
        'revenue_potential_anual': revenue_potential_anual,
        'costs_avoided_anual': costs_avoided_anual,
        
        # Rangos de confianza (NUEVO)
        'rangos': rangos,
        
        # Recuperación
        'recovery_time': recovery_time,
        'recovery_optimista': recovery_optimista,
        'recovery_pesimista': recovery_pesimista,
        'target_util': target_util * 100,
        
        # Indicadores
        'utilization_gap': utilization_gap,
        'efficiency_ratio': avg_util_pct,
    }