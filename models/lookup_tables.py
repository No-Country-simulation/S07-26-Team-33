"""
Tablas de referencia del modelo
"""

import pandas as pd

# ============================================
# PUE POR COOLING + CLIMA
# ============================================

PUE_TABLE = {
    ('Air-cooled', 'Frío'): 1.15,
    ('Air-cooled', 'Templado'): 1.25,
    ('Air-cooled', 'Cálido'): 1.35,
    ('Liquid-cooled', 'Frío'): 1.05,
    ('Liquid-cooled', 'Templado'): 1.08,
    ('Liquid-cooled', 'Cálido'): 1.12,
    ('Hybrid', 'Frío'): 1.09,
    ('Hybrid', 'Templado'): 1.15,
    ('Hybrid', 'Cálido'): 1.22,
}

# ============================================
# CLIMA POR PAÍS
# ============================================

CLIMA_TABLE = {
    'Argentina': 'Templado',
    'Brasil': 'Cálido',
    'Canadá': 'Frío',
    'Colombia': 'Cálido',
    'Francia': 'Templado',
    'Alemania': 'Templado',
    'Irlanda': 'Frío',
    'Portugal': 'Templado',
    'Suecia': 'Frío',
    'Turquía': 'Templado',
    'Nigeria': 'Cálido',
    'Tailandia': 'Cálido',
}

# ============================================
# PEAK DELTA POR TIER
# ============================================

PEAK_DELTA_TABLE = {
    'Tier I': 0.18,
    'Tier II': 0.16,
    'Tier III': 0.14,
    'Tier IV': 0.12,
}

# ============================================
# SAFETY MARGIN POR TIER
# ============================================

SAFETY_MARGIN_TABLE = {
    'Tier I': 0.15,
    'Tier II': 0.18,
    'Tier III': 0.20,
    'Tier IV': 0.25,
}

# ============================================
# BENCHMARK POR TIER
# ============================================

BENCHMARK_TABLE = {
    'Tier I': 0.45,
    'Tier II': 0.55,
    'Tier III': 0.62,
    'Tier IV': 0.85,
}

# ============================================
# GROWTH RATE POR DEMANDA
# ============================================

GROWTH_RATE_TABLE = {
    'Baja': 0.2178,
    'Media': 0.2206,
    'Alta': 0.2223,
    'Muy Alta': 0.2246,
}

# ============================================
# FUNCIONES DE BÚSQUEDA
# ============================================

def get_pue(cooling_type, climate):
    """Obtiene PUE según tipo de cooling y clima"""
    return PUE_TABLE.get((cooling_type, climate), 1.30)

def get_clima(pais):
    """Obtiene clasificación climática por país"""
    return CLIMA_TABLE.get(pais, 'Templado')

def get_peak_delta(tier):
    """Obtiene Peak Delta por Tier"""
    return PEAK_DELTA_TABLE.get(tier, 0.14)

def get_safety_margin(tier):
    """Obtiene Safety Margin por Tier"""
    return SAFETY_MARGIN_TABLE.get(tier, 0.20)

def get_benchmark(tier):
    """Obtiene Benchmark de utilización por Tier"""
    return BENCHMARK_TABLE.get(tier, 0.62)

def get_growth_rate(market_demand):
    """Obtiene tasa de crecimiento por nivel de demanda"""
    return GROWTH_RATE_TABLE.get(market_demand, 0.2206)