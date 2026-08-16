"""
Carga y gestión de los 6 datasets
"""

import pandas as pd
import json
from pathlib import Path

# Ruta base
BASE_PATH = Path(__file__).parent.parent / 'data'

# ============================================
# FUNCIÓN AUXILIAR PARA CARGAR JSON
# ============================================

def cargar_json(path):
    """Carga un archivo JSON con la estructura correcta"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Si tiene la clave 'datos_completos', usarla
    if 'datos_completos' in data:
        df = pd.DataFrame(data['datos_completos'])
    else:
        df = pd.DataFrame(data)
    
    # ============================================
    # CONVERTIR COLUMNAS NUMÉRICAS
    # ============================================
    
    # Lista de columnas que deberían ser numéricas
    columnas_numericas = [
        'average_utilization_pct',
        'peak_utilization_pct',
        'valley_utilization_pct',
        'min_utilization_observed_pct',
        'max_utilization_observed_pct',
        'utilization_std_dev',
        'utilization_range_pct',
        'used_capacity_mw',
        'idle_capacity_mw',
        'idle_capacity_pct',
        'num_racks',
        'densidad_rack_kw',
        'pue',
        'energia_anual_mwh',
        'tarifa_electricidad_usd_kwh',
        'opex_energia_usd_anio',
        'opex_total_usd_por_mw_anio',
        'capex_usd_por_mw',
        'costo_idle_capacity_usd_por_mw_anio',
        'ingreso_usd_por_mw_anio',
        'tco_anual_usd_por_mw',
        'carbon_intensity_g_co2_kwh',
        'emisiones_co2_tons_anio',
        'growth_rate_yoy_pct',
        'uptime_pct',
        'seasonal_factor',
        'capacidad_total_mw',
        'carga_util_mw',
        'pct_carga_util',
        'costo_usd_por_mw',
        'costo_usd_por_mw_min',
        'costo_usd_por_mw_max',
        'factor_escala',
        'factor_region',
        'factor_anio',
        'costo_por_mw_usd',
        'costo_por_sqft_usd',
        'costo_por_rack_usd',
        'pct_land',
        'pct_shell_core',
        'pct_electrical',
        'pct_mechanical_cooling',
        'pct_networking',
        'pct_security',
        'pct_commissioning',
        'pct_contingency',
        'total_sqft',
        'sqft_por_mw',
        'costo_total_usd',
        'costo_land_usd',
        'costo_shell_core_usd',
        'costo_electrical_total_usd',
        'costo_mechanical_total_usd',
        'costo_networking_usd',
        'costo_security_usd',
        'costo_commissioning_usd',
        'costo_contingency_usd',
        'costo_transformers_usd',
        'costo_switchgear_usd',
        'costo_ups_usd',
        'costo_generators_usd',
        'costo_pdu_usd',
        'costo_cabling_electrical_usd',
        'costo_chillers_usd',
        'costo_crah_crac_usd',
        'costo_cooling_towers_usd',
        'costo_pumps_usd',
        'costo_containment_usd',
        'costo_bms_usd',
        'costo_mano_obra_total_usd',
        'costo_materiales_total_usd',
        'costo_equipamiento_total_usd',
        'costo_soft_total_usd',
        'meses_construccion',
        'dias_permisos',
        'total_dias_proyecto',
        'pue_estimado',
        'opex_anual_estimado_usd',
        'tco_10_anios_usd',
        'ingreso_anual_estimado_usd',
        'roi_simple_anios',
        'factor_mano_obra',
        'factor_material',
        'factor_impuesto',
        'factor_tier',
        'pct_utilizacion_promedio',
        'utilizacion_peak',
        'utilizacion_valle',
        'rango_utilizacion_pct',
        'peak_vs_avg_ratio',
        'utilizacion_verano',
        'utilizacion_invierno',
        'utilizacion_dia',
        'utilizacion_noche',
        'seasonal_amplitude',
        'day_night_amplitude',
        'utilizacion_min_observada',
        'utilizacion_max_observada',
        'carga_inactiva_mw',
        'pct_inactivo',
        'costo_mw_inactivo_anio',
        'eficiencia_kw_cooling_por_kw_it',
        'consumo_cooling_mw',
        'consumo_cooling_pct_it',
        'temp_ambiente_c',
        'temp_suministro_c',
        'temp_retorno_c',
        'delta_t_c',
        'humedad_relativa_pct',
        'free_cooling_hours_anio',
        'capex_cooling_usd_por_mw',
        'capex_cooling_pct_total',
        'opex_cooling_usd_por_mw_anio',
        'tco_cooling_usd_por_mw_anio',
        'emisiones_cooling_tons_co2_anio',
        'factor_anio_eficiencia',
        'power_it_mw',
        'power_cooling_mw',
        'power_other_mw',
        'power_total_mw',
        'other_overhead_pct_it',
        'wue',
        'temp_ambiente_avg_c',
        'temp_ambiente_max_c',
        'temp_ambiente_min_c',
        'altitud_m',
        'latitud',
        'free_cooling_pct',
        'capex_total_usd_por_mw',
        'opex_energia_usd_por_mw_anio',
        'tco_anual_usd_por_mw',
        'commitment_level',
        'capacidad_bin',
        'densidad_bin',
        'pue_bin',
        'renovable_bin',
        'eficiencia_bin',
        'util_bin'
    ]
    
    # Convertir columnas numéricas
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# ============================================
# CARGA DE DATASETS
# ============================================

def load_dataset_1():
    """Dataset 1: Average Utilization"""
    path = BASE_PATH / 'data_1.json'
    return cargar_json(path)

def load_dataset_2():
    """Dataset 2: Utilization Range Summary"""
    path = BASE_PATH / 'data_2.json'
    return cargar_json(path)

def load_dataset_3():
    """Dataset 3: Precio Construcción / CapEx"""
    path = BASE_PATH / 'data_3.json'
    return cargar_json(path)

def load_dataset_4():
    """Dataset 4: Cooling Efficiency / PUE"""
    path = BASE_PATH / 'data_4.json'
    return cargar_json(path)

def load_dataset_5():
    """Dataset 5: PUE Actual / Argentina"""
    path = BASE_PATH / 'data_5.json'
    return cargar_json(path)

def load_dataset_6():
    """Dataset 6: Utilization Range"""
    path = BASE_PATH / 'data_6.json'
    return cargar_json(path)

# ============================================
# BÚSQUEDAS ESPECÍFICAS
# ============================================

def get_tarifa_by_country(pais):
    """Obtiene tarifa eléctrica por país desde dataset 4"""
    df = load_dataset_4()
    resultado = df[df['pais'].str.lower() == pais.lower()]
    if not resultado.empty:
        if 'tarifa_electricidad_usd_kwh' in resultado.columns:
            val = resultado.iloc[0]['tarifa_electricidad_usd_kwh']
            if pd.notna(val):
                return float(val)
        elif 'tarifa_electricidad' in resultado.columns:
            val = resultado.iloc[0]['tarifa_electricidad']
            if pd.notna(val):
                return float(val)
    return 0.10

def get_capex_by_country_tier(pais, tier):
    """Obtiene CapEx por MW desde dataset 3"""
    df = load_dataset_3()
    resultado = df[(df['pais'].str.lower() == pais.lower()) & 
                   (df['tier'].str.lower() == tier.lower())]
    if not resultado.empty:
        if 'costo_por_mw_usd' in resultado.columns:
            val = resultado.iloc[0]['costo_por_mw_usd']
            if pd.notna(val):
                return float(val)
        elif 'costo_usd_por_mw' in resultado.columns:
            val = resultado.iloc[0]['costo_usd_por_mw']
            if pd.notna(val):
                return float(val)
    return 4_000_000

def get_revenue_by_country_tier(pais, tier):
    """Obtiene Revenue por MW desde dataset 3"""
    df = load_dataset_3()
    resultado = df[(df['pais'].str.lower() == pais.lower()) & 
                   (df['tier'].str.lower() == tier.lower())]
    if not resultado.empty:
        if 'ingreso_usd_por_mw_anio' in resultado.columns:
            val = resultado.iloc[0]['ingreso_usd_por_mw_anio']
            if pd.notna(val):
                return float(val)
    return 0

# ============================================
# DATOS PARA GRÁFICOS
# ============================================

def get_workload_data():
    """Obtiene datos de workload para heatmap"""
    df = load_dataset_1()
    if 'workload_principal' in df.columns and 'tier' in df.columns and 'average_utilization_pct' in df.columns:
        pivot = df.pivot_table(
            values='average_utilization_pct',
            index='workload_principal',
            columns='tier',
            aggfunc='mean'
        )
        return pivot
    return pd.DataFrame()

def get_country_comparison():
    """Obtiene datos de comparativa por país"""
    df = load_dataset_1()
    if 'pais' in df.columns and 'average_utilization_pct' in df.columns:
        return df.groupby('pais')['average_utilization_pct'].mean().sort_values(ascending=False)
    return pd.Series()