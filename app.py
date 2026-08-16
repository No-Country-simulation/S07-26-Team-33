"""
Data Center Analytics - Stranded Capacity Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np

# ============================================
# IMPORTAR MÓDULOS
# ============================================

from models.calculator import calcular_todo
from models.datasets import (
    load_dataset_1,
    load_dataset_2,
    load_dataset_3,
    load_dataset_4,
    load_dataset_5,
    load_dataset_6,
    get_tarifa_by_country,
    get_capex_by_country_tier
)
from models.lookup_tables import get_clima, get_benchmark
from components.charts import (
    crear_donut_capacidad,
    crear_barras_comparativa,
    crear_tornado_chart,
    crear_monte_carlo,
    crear_barras_desglose,
    crear_heatmap_capex,
    crear_area_evolucion,
    crear_lineas_recuperacion,
    crear_heatmap_workload,
    crear_matriz_oportunidades,
    crear_barras_paises
)

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Data Center Analytics - Stranded Capacity",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CARGAR ESTILOS CSS
# ============================================

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .stApp { background: #f0f2f5; min-height: 100vh; }
        [data-testid="stPlotlyChart"] {
            background: white; border-radius: 12px; padding: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
        }
        
        .main-header {
            display: flex; align-items: center; gap: 15px; margin-bottom: 25px;
            padding: 20px 28px; background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 50%, #1e3a5f 100%);
            border-radius: 14px; box-shadow: 0 4px 25px rgba(30,58,95,0.25);
            flex-wrap: wrap; color: white;
        }
        .main-header i { font-size: 32px; color: #60a5fa; }
        .main-header .title { font-size: 26px; font-weight: 800; color: white; }
        .main-header .title span { color: #93c5fd; }
        .main-header .badge {
            font-size: 11px; color: #bfdbfe; background: rgba(255,255,255,0.08);
            padding: 5px 14px; border-radius: 20px; font-weight: 600; margin-left: auto;
        }
        
        .banner-alert {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 50%, #1e3a5f 100%);
            border-radius: 14px; padding: 18px 24px; margin-bottom: 20px; color: white;
        }
        .banner-title { font-size: 18px; font-weight: 700; margin-bottom: 4px; color: white; }
        .banner-subtitle { font-size: 13px; color: rgba(255,255,255,0.7); margin-bottom: 10px; }
        .banner-stats { display: flex; gap: 12px; margin: 8px 0; flex-wrap: wrap; }
        .banner-stat {
            background: rgba(255,255,255,0.08); padding: 5px 14px; border-radius: 20px;
            font-size: 12px; color: rgba(255,255,255,0.8);
        }
        .banner-stat strong { color: white; }
        .banner-bar { width: 100%; height: 5px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 10px; overflow: hidden; }
        .banner-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #60a5fa, #a78bfa, #f87171); transition: width 0.8s ease; }
        
        .control-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 100%);
            border-radius: 12px; padding: 14px 18px; margin-bottom: 12px;
            box-shadow: 0 2px 15px rgba(30,58,95,0.15);
        }
        .control-card-title { font-size: 13px; font-weight: 700; color: #93c5fd; margin-bottom: 12px; }
        
        .options-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 100%);
            border-radius: 12px; padding: 12px 16px; box-shadow: 0 2px 15px rgba(30,58,95,0.15);
        }
        .options-card .title {
            font-size: 13px; font-weight: 700; color: #93c5fd; margin-bottom: 10px;
        }
        
        .control-card .stSelectbox label,
        .control-card .stNumberInput label,
        .control-card .stSlider label,
        .options-card .stCheckbox label {
            color: white !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }
        .control-card .stSelectbox label p,
        .control-card .stNumberInput label p,
        .control-card .stSlider label p,
        .options-card .stCheckbox label p {
            color: white !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }
        .options-card .stCheckbox label:hover,
        .options-card .stCheckbox label:hover p {
            color: #93c5fd !important;
        }
        
        .stSelectbox > div > div {
            background: white !important; border-color: #d1d5db !important;
            color: #1e3a5f !important; border-radius: 8px;
        }
        .stNumberInput > div > div > input {
            background: white !important; border-color: #d1d5db !important;
            color: #1e3a5f !important; border-radius: 8px; font-weight: 600;
        }
        
        .stButton > button {
            border-radius: 10px; font-weight: 700 !important; padding: 10px 20px;
            font-size: 14px; border: none !important; width: 100%;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #ef4444, #dc2626) !important; color: white !important;
        }
        .stButton > button[kind="secondary"] {
            background: linear-gradient(135deg, #1e3a5f, #2d4a7a) !important;
            color: #93c5fd !important; border: 2px solid #3b5998 !important;
        }
        
        .country-card-horizontal {
            background: linear-gradient(135deg, #1e3a5f 0%, #3b5998 50%, #2d4a7a 100%);
            border-radius: 14px; padding: 20px; margin: 16px 0; color: white;
        }
        .country-items { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 16px; }
        .country-item {
            background: rgba(255,255,255,0.08); border-radius: 10px; padding: 14px; text-align: center;
        }
        .country-item .item-icon { font-size: 22px; color: #93c5fd; margin-bottom: 6px; }
        .country-item .item-label { font-size: 9px; color: rgba(255,255,255,0.5); font-weight: 600; text-transform: uppercase; }
        .country-item .item-value { font-size: 14px; font-weight: 700; color: white; }
        .workload-tag {
            display: inline-block; background: rgba(96,165,250,0.15); color: #93c5fd;
            padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; margin: 2px;
        }
        
        .kpi-card { border-radius: 14px; padding: 16px 18px; color: white; min-height: 100px; }
        .kpi-label { font-size: 10px; font-weight: 600; text-transform: uppercase; opacity: 0.8; }
        .kpi-value { font-size: 28px; font-weight: 800; margin: 2px 0; }
        .kpi-sub { font-size: 12px; opacity: 0.7; }
        .kpi-stranded { background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); }
        .kpi-capital { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }
        .kpi-oportunidad { background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); }
        .kpi-gap { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); }
        
        .section-title {
            font-size: 16px; font-weight: 700; color: white; margin: 24px 0 16px 0;
            padding: 14px 18px; background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 50%, #3b5998 100%);
            border-radius: 12px; border-left: 4px solid #60a5fa;
        }
        
        .footer {
            margin-top: 32px; padding: 20px; text-align: center; color: #bfdbfe; font-size: 12px;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 100%); border-radius: 14px;
        }
        
        [data-testid="stSidebar"] { display: none !important; }
        
        @media (max-width: 768px) {
            .country-items { grid-template-columns: repeat(2, 1fr); }
            .kpi-value { font-size: 22px; }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

st.markdown(
    """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">""",
    unsafe_allow_html=True
)

# ============================================
# CARGAR LOS 6 DATASETS REALES
# ============================================

@st.cache_data
def cargar_todos_datos():
    df1 = load_dataset_1()
    df2 = load_dataset_2()
    df3 = load_dataset_3()
    df4 = load_dataset_4()
    df5 = load_dataset_5()
    df6 = load_dataset_6()
    return df1, df2, df3, df4, df5, df6

try:
    df1, df2, df3, df4, df5, df6 = cargar_todos_datos()
except Exception as e:
    st.warning(f"Error cargando datos: {e}")
    df1 = df2 = df3 = df4 = df5 = df6 = pd.DataFrame()

# ============================================
# LISTAS DINÁMICAS
# ============================================

if not df1.empty and 'pais' in df1.columns:
    PAISES_DISPONIBLES = sorted(df1['pais'].unique().tolist())
else:
    PAISES_DISPONIBLES = ['Argentina', 'Brazil', 'Colombia', 'Ireland', 'Portugal', 'Sweden', 'Turkey']

if not df1.empty and 'tier' in df1.columns:
    TIERS_DISPONIBLES = sorted(df1['tier'].unique().tolist())
else:
    TIERS_DISPONIBLES = ['Tier I', 'Tier II', 'Tier III', 'Tier IV']

# ============================================
# INICIALIZAR ESTADO
# ============================================

if 'params' not in st.session_state:
    st.session_state['params'] = {
        'facility_mw': 100.0,
        'avg_util_pct': 55,
        'cooling_type': 'Air-cooled',
        'pais': PAISES_DISPONIBLES[0] if PAISES_DISPONIBLES else 'Brazil',
        'tier': 'Tier III',
        'market_demand': 'Media',
        'mostrar_rangos': True,
        'comparar_pares': True,
        'proyectar_escenarios': True,
        'incluir_sensibilidad': True
    }

if 'resultados' not in st.session_state:
    st.session_state['resultados'] = None

if 'tab_activa' not in st.session_state:
    st.session_state['tab_activa'] = 0

# ============================================
# FUNCIÓN PARA OBTENER DATOS REALES
# ============================================

def obtener_datos_pais_completo(pais, tier, df1, df2, df3, df4, df5, df6):
    datos = {}
    pais_lower = pais.lower()
    
    if not df1.empty and 'pais' in df1.columns:
        datos_pais1 = df1[df1['pais'].str.lower() == pais_lower]
        if not datos_pais1.empty:
            if 'average_utilization_pct' in df1.columns:
                datos['avg_util'] = datos_pais1['average_utilization_pct'].mean()
            if 'tarifa_electricidad_usd_kwh' in df1.columns:
                datos['tarifa'] = datos_pais1['tarifa_electricidad_usd_kwh'].mean()
            if 'pue' in df1.columns:
                datos['pue'] = datos_pais1['pue'].mean()
            if 'workload_principal' in df1.columns:
                datos['workloads'] = datos_pais1['workload_principal'].value_counts().head(3).index.tolist()
            if 'growth_rate_yoy_pct' in df1.columns:
                datos['growth_rate'] = datos_pais1['growth_rate_yoy_pct'].mean() / 100
            datos['registros'] = len(datos_pais1)
    
    if not df4.empty and 'pais' in df4.columns and 'costo_por_mw_usd' in df4.columns:
        datos_pais4 = df4[df4['pais'].str.lower() == pais_lower]
        if not datos_pais4.empty:
            datos['capex_mw'] = datos_pais4['costo_por_mw_usd'].mean()
    
    if 'capex_mw' not in datos and not df2.empty:
        if 'pais' in df2.columns and 'costo_usd_por_mw' in df2.columns:
            datos_pais2 = df2[df2['pais'].str.lower() == pais_lower]
            if not datos_pais2.empty:
                datos['capex_mw'] = datos_pais2['costo_usd_por_mw'].mean()
    
    if not df3.empty and 'pais' in df3.columns and 'clima' in df3.columns:
        datos_pais3 = df3[df3['pais'].str.lower() == pais_lower]
        if not datos_pais3.empty:
            datos['clima'] = datos_pais3['clima'].iloc[0]
    
    datos.setdefault('avg_util', 55)
    datos.setdefault('tarifa', get_tarifa_by_country(pais))
    datos.setdefault('pue', 1.5)
    datos.setdefault('workloads', ['No disponible'])
    datos.setdefault('growth_rate', 0.05)
    datos.setdefault('registros', 0)
    datos.setdefault('capex_mw', get_capex_by_country_tier(pais, tier))
    datos.setdefault('clima', get_clima(pais))
    
    return datos

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="main-header">
    <i class="fa-solid fa-microchip"></i>
    <span class="title">Data Center <span>Analytics</span></span>
    <span class="badge">
        <i class="fa-solid fa-database"></i> Stranded Capacity Intelligence
    </span>
</div>
""", unsafe_allow_html=True)

# ============================================
# TABS
# ============================================

tab_col1, tab_col2 = st.columns(2)

with tab_col1:
    if st.button("Vista Ejecutiva", width='stretch', 
                 type="primary" if st.session_state['tab_activa'] == 0 else "secondary"):
        st.session_state['tab_activa'] = 0
        st.rerun()

with tab_col2:
    if st.button("Análisis Avanzado", width='stretch',
                 type="primary" if st.session_state['tab_activa'] == 1 else "secondary"):
        st.session_state['tab_activa'] = 1
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# PANEL DE CONTROL
# ============================================

st.markdown("""
<div class="control-card">
    <div class="control-card-title">
        <i class="fa-solid fa-sliders"></i> Panel de Control
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    facility_mw = st.number_input(
        "Capacidad Total (MW)",
        min_value=1.0, max_value=1000.0,
        value=float(st.session_state['params']['facility_mw']),
        step=1.0, format="%.2f"
    )
    avg_util_pct = st.slider(
        "Utilización Promedio (%)",
        min_value=0, max_value=100,
        value=int(st.session_state['params']['avg_util_pct']), step=1
    )

with col2:
    cooling_type = st.selectbox(
        "Tipo de Refrigeración",
        options=["Air-cooled", "Liquid-cooled", "Hybrid"],
        index=["Air-cooled", "Liquid-cooled", "Hybrid"].index(st.session_state['params']['cooling_type'])
    )
    pais = st.selectbox(
        "País",
        options=PAISES_DISPONIBLES,
        index=PAISES_DISPONIBLES.index(st.session_state['params']['pais'])
        if st.session_state['params']['pais'] in PAISES_DISPONIBLES else 0
    )

with col3:
    tier = st.selectbox(
        "Nivel de Disponibilidad (Tier)",
        options=TIERS_DISPONIBLES,
        index=TIERS_DISPONIBLES.index(st.session_state['params']['tier'])
        if st.session_state['params']['tier'] in TIERS_DISPONIBLES else 0
    )
    market_demand = st.selectbox(
        "Demanda de Mercado",
        options=["Baja", "Media", "Alta", "Muy Alta"],
        index=["Baja", "Media", "Alta", "Muy Alta"].index(st.session_state['params']['market_demand'])
    )

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# OPCIONES DE ANÁLISIS
# ============================================

st.markdown("""
<div class="options-card">
    <div class="title">
        <i class="fa-solid fa-chart-pie"></i> Opciones de Análisis
    </div>
""", unsafe_allow_html=True)

col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)

with col_opt1:
    comparar_pares = st.checkbox("Comparar con pares", value=st.session_state['params']['comparar_pares'])
with col_opt2:
    mostrar_rangos = st.checkbox("Mostrar rangos", value=st.session_state['params']['mostrar_rangos'])
with col_opt3:
    proyectar_escenarios = st.checkbox("Proyectar escenarios", value=st.session_state['params']['proyectar_escenarios'])
with col_opt4:
    incluir_sensibilidad = st.checkbox("Análisis sensibilidad", value=st.session_state['params']['incluir_sensibilidad'])

st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# GUARDAR PARÁMETROS
# ============================================

st.session_state['params'] = {
    'facility_mw': facility_mw,
    'avg_util_pct': avg_util_pct,
    'cooling_type': cooling_type,
    'pais': pais,
    'tier': tier,
    'market_demand': market_demand,
    'mostrar_rangos': mostrar_rangos,
    'comparar_pares': comparar_pares,
    'proyectar_escenarios': proyectar_escenarios,
    'incluir_sensibilidad': incluir_sensibilidad
}

# ============================================
# OBTENER DATOS REALES
# ============================================

datos_pais = obtener_datos_pais_completo(pais, tier, df1, df2, df3, df4, df5, df6)

# ============================================
# CALCULAR RESULTADOS USANDO EL MOTOR CORREGIDO
# ============================================

# AHORA usamos calcular_todo() en lugar de cálculos manuales
resultados = calcular_todo(
    facility_mw=float(facility_mw),
    avg_util_pct=float(avg_util_pct),
    cooling_type=cooling_type,
    pais=pais,
    tier=tier,
    market_demand=market_demand
)

# Sobrescribir algunos datos con los reales de los datasets
resultados['tarifa'] = datos_pais['tarifa']
resultados['pue'] = datos_pais['pue']
resultados['clima'] = datos_pais['clima']
resultados['workloads'] = datos_pais['workloads']
resultados['registros'] = datos_pais['registros']

st.session_state['resultados'] = resultados

# ============================================
# EXTRAER VARIABLES PARA EL DASHBOARD
# ============================================

stranded_mw = resultados.get('stranded_mw', 0)
stranded_pct = resultados.get('stranded_pct', 0)
stranded_capex = resultados.get('stranded_capex', 0)
costo_oportunidad_anual = resultados.get('costo_oportunidad_anual', 0)
perdida_anual_total = resultados.get('perdida_anual_total', 0)
recovery_time = resultados.get('recovery_time', 0)
benchmark_diff = resultados.get('utilization_gap', 0)
benchmark_avg = resultados.get('benchmark', 0.62) * 100
avg_util_pct_f = resultados.get('avg_util_pct', 55)
growth_rate_real = resultados.get('growth_rate', 0.05)
pue_real = resultados.get('pue', 1.5)
tarifa_real = resultados.get('tarifa', 0.10)
capex_real = resultados.get('capex_per_mw', 4000000)
tier = resultados.get('tier', 'Tier III')
pais = resultados.get('pais', '')

# Obtener rangos
rangos = resultados.get('rangos', {})
rango_stranded = rangos.get('stranded_mw', {'central': stranded_mw, 'inferior': stranded_mw * 0.88, 'superior': stranded_mw * 1.12})
rango_capital = rangos.get('stranded_capex', {'central': stranded_capex, 'inferior': stranded_capex * 0.90, 'superior': stranded_capex * 1.10})
rango_oportunidad = rangos.get('costo_oportunidad_anual', {'central': costo_oportunidad_anual, 'inferior': costo_oportunidad_anual * 0.85, 'superior': costo_oportunidad_anual * 1.15})

# ============================================
# BANNER DINÁMICO (CORREGIDO)
# ============================================

if stranded_pct >= 40:
    icono = 'fa-circle-exclamation'
    icono_color = '#f87171'
    titulo = 'Alerta Crítica de Capacidad Stranded'
    severidad = 'Crítica'
    badge_color = '#f87171'
elif stranded_pct >= 30:
    icono = 'fa-triangle-exclamation'
    icono_color = '#fb923c'
    titulo = 'Advertencia de Capacidad Stranded'
    severidad = 'Alta'
    badge_color = '#fb923c'
elif stranded_pct >= 20:
    icono = 'fa-triangle-exclamation'
    icono_color = '#fbbf24'
    titulo = 'Atención: Capacidad Subutilizada'
    severidad = 'Media'
    badge_color = '#fbbf24'
elif stranded_pct >= 10:
    icono = 'fa-circle-info'
    icono_color = '#60a5fa'
    titulo = 'Capacidad Ligeramente Subutilizada'
    severidad = 'Leve'
    badge_color = '#60a5fa'
else:
    icono = 'fa-circle-check'
    icono_color = '#34d399'
    titulo = 'Capacidad Saludable'
    severidad = 'Óptima'
    badge_color = '#34d399'

banner_html = f"""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}
    
    @keyframes iconPulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.08); }}
    }}
    
    body {{
        margin: 0;
        padding: 0;
        font-family: 'Inter', sans-serif;
    }}
    
    .banner {{
        background: linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 50%, #1e3a5f 100%);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 20px;
        color: white;
        border-left: 6px solid #60a5fa;
        box-shadow: 0 12px 40px rgba(30, 58, 95, 0.3);
    }}
    
    .banner-title {{
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 14px;
        letter-spacing: 0.3px;
    }}
    
    .banner-title i {{
        font-size: 28px;
        color: {icono_color};
        animation: iconPulse 2s ease-in-out infinite;
    }}
    
    .severidad-badge {{
        display: inline-block;
        background: {badge_color}20;
        border: 1px solid {badge_color};
        color: {badge_color};
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 6px;
    }}
    
    .banner-subtitle {{
        font-size: 14px;
        opacity: 0.85;
        margin-bottom: 14px;
        line-height: 1.5;
    }}
    
    .banner-subtitle i {{
        color: #93c5fd;
    }}
    
    .banner-stats {{
        display: flex;
        gap: 10px;
        margin: 14px 0;
        flex-wrap: wrap;
    }}
    
    .banner-stat {{
        background: rgba(255, 255, 255, 0.08);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }}
    
    .banner-stat:hover {{
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }}
    
    .banner-stat i {{
        color: #60a5fa;
        font-size: 14px;
    }}
    
    .banner-stat strong {{
        font-weight: 700;
    }}
    
    .banner-bar {{
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        margin-top: 14px;
        overflow: hidden;
    }}
    
    .banner-bar-fill {{
        height: 100%;
        width: {stranded_pct}%;
        border-radius: 6px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #60a5fa);
        animation: shimmer 2s linear infinite;
        background-size: 200% auto;
        transition: width 0.5s ease;
    }}
    
    .banner-footer {{
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        opacity: 0.7;
        margin-top: 10px;
        flex-wrap: wrap;
        gap: 8px;
    }}
    
    .banner-footer i {{
        color: #93c5fd;
        margin-right: 4px;
    }}
</style>
</head>
<body>
<div class="banner">
    <div class="banner-title">
        <i class="fa-solid {icono}"></i>
        <div>
            {titulo}
            <div>
                <span class="severidad-badge">{severidad}</span>
            </div>
        </div>
    </div>
    
    <div class="banner-subtitle">
        <i class="fa-solid fa-location-dot"></i> 
        <strong>{pais}</strong> · {tier} · 
        Tu datacenter tiene <strong style="color: #93c5fd; font-size: 16px;">{stranded_mw:.1f} MW</strong> sin utilizar 
        (<strong style="color: #93c5fd;">{stranded_pct:.1f}%</strong> de tu capacidad total)
    </div>
    
    <div class="banner-stats">
        <span class="banner-stat">
            <i class="fa-solid fa-building"></i> 
            <strong>${stranded_capex/1e6:.1f} M</strong> capital inmovilizado
        </span>
        <span class="banner-stat">
            <i class="fa-solid fa-clock"></i> 
            <strong>{recovery_time:.1f} años</strong> recuperación
        </span>
        <span class="banner-stat">
            <i class="fa-solid fa-chart-simple"></i> 
            <strong>{benchmark_diff:+.1f}%</strong> vs benchmark
        </span>
        <span class="banner-stat">
            <i class="fa-solid fa-gauge-high"></i> 
            Utilización: <strong>{avg_util_pct_f:.1f}%</strong>
        </span>
        <span class="banner-stat">
            <i class="fa-solid fa-bolt"></i> 
            PUE: <strong>{pue_real:.2f}</strong>
        </span>
    </div>
    
    <div class="banner-bar">
        <div class="banner-bar-fill"></div>
    </div>
    
    <div class="banner-footer">
        <span><i class="fa-solid fa-chart-line"></i> Utilización: {avg_util_pct_f:.1f}%</span>
        <span><i class="fa-solid fa-target"></i> Benchmark {tier}: {benchmark_avg:.1f}%</span>
        <span><i class="fa-solid fa-arrow-trend-up"></i> Growth: {growth_rate_real*100:.1f}% YoY</span>
        <span><i class="fa-solid fa-percent"></i> Rango: {rango_stranded['inferior']:.1f}-{rango_stranded['superior']:.1f} MW</span>
    </div>
</div>
</body>
</html>
"""

st.html(banner_html)

# ============================================
# KPIs - VERSIÓN CORREGIDA
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card kpi-stranded">
        <div class="kpi-label">Capacidad Stranded</div>
        <div class="kpi-value">{stranded_mw:.1f} MW</div>
        <div class="kpi-sub">Rango: {rango_stranded['inferior']:.1f} - {rango_stranded['superior']:.1f} MW</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card kpi-capital">
        <div class="kpi-label">Capital Inmovilizado</div>
        <div class="kpi-value">${stranded_capex/1e6:.1f} M</div>
        <div class="kpi-sub">Rango: ${rango_capital['inferior']/1e6:.1f}M - ${rango_capital['superior']/1e6:.1f}M</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card kpi-oportunidad">
        <div class="kpi-label">Costo de Oportunidad</div>
        <div class="kpi-value">${costo_oportunidad_anual/1e6:.1f} M/año</div>
        <div class="kpi-sub">Rango: ${rango_oportunidad['inferior']/1e6:.1f}M - ${rango_oportunidad['superior']/1e6:.1f}M/año</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card kpi-gap">
        <div class="kpi-label">Utilization Gap</div>
        <div class="kpi-value">{benchmark_diff:+.1f} pp</div>
        <div class="kpi-sub">Benchmark: {benchmark_avg:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# CONTEXTO DEL PAÍS
# ============================================

capex_en_millones = capex_real / 1000000

st.markdown(f"""
<div class="country-card-horizontal">
    <div class="header">
        <i class="fa-solid fa-location-dot"></i>
        Contexto: {pais}
    </div>
    <div class="country-items">
        <div class="country-item">
            <div class="item-icon"><i class="fa-solid fa-cloud-sun"></i></div>
            <div class="item-label">Clima</div>
            <div class="item-value">{datos_pais['clima']}</div>
        </div>
        <div class="country-item">
            <div class="item-icon"><i class="fa-solid fa-bolt"></i></div>
            <div class="item-label">Tarifa</div>
            <div class="item-value">${tarifa_real:.4f}/kWh</div>
        </div>
        <div class="country-item">
            <div class="item-icon"><i class="fa-solid fa-chart-simple"></i></div>
            <div class="item-label">Utilización</div>
            <div class="item-value">{avg_util_pct_f:.1f}%</div>
        </div>
        <div class="country-item">
            <div class="item-icon"><i class="fa-solid fa-database"></i></div>
            <div class="item-label">Registros</div>
            <div class="item-value">{datos_pais['registros']}</div>
        </div>
        <div class="country-item">
            <div class="item-icon"><i class="fa-solid fa-microchip"></i></div>
            <div class="item-label">CapEx</div>
            <div class="item-value">${capex_en_millones:.1f}M/MW</div>
        </div>
    </div>
    <div class="workload-section">
        <span class="label">
            <i class="fa-solid fa-server"></i> Workloads principales:
        </span>
        {''.join([f'<span class="workload-tag">{w}</span>' for w in datos_pais['workloads']])}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# CONTENIDO SEGÚN TAB CON OPCIONES FUNCIONALES
# ============================================

if st.session_state['tab_activa'] == 0:
    # ============================================
    # VISTA EJECUTIVA
    # ============================================
    
    # Primera fila - SIEMPRE VISIBLE
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-title"><i class="fa-solid fa-chart-pie"></i> Distribución de Capacidad</p>', unsafe_allow_html=True)
        try:
            fig = crear_donut_capacidad(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    with col2:
        st.markdown('<p class="section-title"><i class="fa-solid fa-chart-bar"></i> Comparativa con la Industria</p>', unsafe_allow_html=True)
        try:
            fig = crear_barras_comparativa(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    # ============================================
    # OPCIÓN: Comparar con pares
    # ============================================
    if comparar_pares:
        st.markdown('<p class="section-title"><i class="fa-solid fa-globe"></i> Comparativa por País</p>', unsafe_allow_html=True)
        try:
            fig = crear_barras_paises(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    # ============================================
    # OPCIONES: Proyectar escenarios + Análisis sensibilidad
    # ============================================
    col1, col2 = st.columns(2)
    
    if proyectar_escenarios:
        with col1:
            st.markdown('<p class="section-title"><i class="fa-solid fa-timeline"></i> Proyección de Escenarios</p>', unsafe_allow_html=True)
            try:
                fig = crear_lineas_recuperacion(resultados)
                st.plotly_chart(fig, width='stretch', height=450)
            except Exception as e:
                st.warning(f"Error: {e}")
    
    if incluir_sensibilidad:
        with col2:
            st.markdown('<p class="section-title"><i class="fa-solid fa-crosshairs"></i> Análisis de Sensibilidad</p>', unsafe_allow_html=True)
            try:
                fig = crear_tornado_chart(resultados)
                st.plotly_chart(fig, width='stretch', height=450)
            except Exception as e:
                st.warning(f"Error: {e}")
    
    # Matriz de Oportunidades - SIEMPRE VISIBLE
    st.markdown('<p class="section-title"><i class="fa-solid fa-bullseye"></i> Matriz de Oportunidades</p>', unsafe_allow_html=True)
    try:
        fig = crear_matriz_oportunidades(resultados)
        st.plotly_chart(fig, width='stretch', height=550)
    except Exception as e:
        st.warning(f"Error: {e}")

else:
    # ============================================
    # ANÁLISIS AVANZADO
    # ============================================
    
    # Primera fila - SIEMPRE VISIBLE
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-title"><i class="fa-solid fa-crosshairs"></i> ¿Qué variable impacta más?</p>', unsafe_allow_html=True)
        try:
            fig = crear_tornado_chart(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    with col2:
        st.markdown('<p class="section-title"><i class="fa-solid fa-chart-line"></i> Rango de Incertidumbre</p>', unsafe_allow_html=True)
        try:
            fig = crear_monte_carlo(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Segunda fila - SIEMPRE VISIBLE
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="section-title"><i class="fa-solid fa-money-bill-trend-up"></i> Desglose de Costos</p>', unsafe_allow_html=True)
        try:
            fig = crear_barras_desglose(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    with col2:
        st.markdown('<p class="section-title"><i class="fa-solid fa-building"></i> CapEx por País y Tier</p>', unsafe_allow_html=True)
        try:
            fig = crear_heatmap_capex(resultados)
            st.plotly_chart(fig, width='stretch', height=500)
        except Exception as e:
            st.warning(f"Error: {e}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tercera fila - CONDICIONAL según "Mostrar rangos"
    if mostrar_rangos:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="section-title"><i class="fa-solid fa-clock-rotate-left"></i> Evolución Histórica</p>', unsafe_allow_html=True)
            try:
                fig = crear_area_evolucion(resultados)
                st.plotly_chart(fig, width='stretch', height=450)
            except Exception as e:
                st.warning(f"Error: {e}")
        
        with col2:
            st.markdown('<p class="section-title"><i class="fa-solid fa-timeline"></i> Proyección Recuperación</p>', unsafe_allow_html=True)
            try:
                fig = crear_lineas_recuperacion(resultados)
                st.plotly_chart(fig, width='stretch', height=450)
            except Exception as e:
                st.warning(f"Error: {e}")
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabla Workload - SIEMPRE VISIBLE
    st.markdown('<p class="section-title"><i class="fa-solid fa-fire"></i> Workload vs Tier</p>', unsafe_allow_html=True)
    try:
        fig = crear_heatmap_workload(resultados)
        st.plotly_chart(fig, width='stretch', height=550)
    except Exception as e:
        st.warning(f"Error: {e}")

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    <i class="fa-regular fa-copyright"></i> 2026 · Data Center Analytics
    <span style="margin: 0 15px;">|</span>
    <i class="fa-solid fa-database"></i> Datos reales de 6 datasets
    <span style="margin: 0 15px;">|</span>
    <i class="fa-solid fa-chart-simple"></i> v2.0 · Tech Edition
</div>
""", unsafe_allow_html=True)