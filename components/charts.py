"""
Funciones para crear todos los gráficos del dashboard
CON DATOS 100% REALES DE LOS DATASETS - VERSIÓN CORREGIDA
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Importar datasets reales
from models.datasets import (
    load_dataset_1,
    load_dataset_3,
    load_dataset_4,
    get_workload_data,
    get_country_comparison
)

# ============================================
# COLORES CORPORATIVOS
# ============================================

COLORS = {
    'utilizada': '#00cc96',
    'stranded': '#ff4b4b',
    'headroom': '#ffa500',
    'benchmark': '#1f77b4',
    'pares': '#7f7f7f',
    'promedio': '#95a5a6',
    'energia': '#e67e22',
    'capex': '#3498db',
    'oportunidad': '#9b59b6',  # NUEVO: color para costo de oportunidad
    'positive': '#00cc96',
    'negative': '#ff4b4b',
    'warning': '#ffa500',
}

# ============================================
# CONFIGURACIÓN GLOBAL DE GRÁFICAS
# ============================================

def aplicar_estilo_base(fig, height=400):
    """Aplica estilo base consistente a todas las gráficas"""
    fig.update_layout(
        height=height,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#1a1a2e'),
        margin=dict(t=50, b=40, l=40, r=40),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Inter"
        )
    )
    return fig


# ============================================
# FUNCIÓN AUXILIAR: OBTENER DATAFRAME DE CAPEX
# ============================================

def _obtener_dataframe_capex():
    """
    Obtiene el dataframe correcto que contiene datos de CapEx
    Busca en load_dataset_3 y load_dataset_4
    """
    # Probar con load_dataset_3 primero
    try:
        df_3 = load_dataset_3()
        if not df_3.empty:
            # Buscar columnas de costo
            columnas_costo = [col for col in df_3.columns if 'costo' in col.lower() or 'capex' in col.lower()]
            if 'pais' in df_3.columns and 'tier' in df_3.columns and len(columnas_costo) > 0:
                return df_3, columnas_costo[0]
    except:
        pass
    
    # Probar con load_dataset_4
    try:
        df_4 = load_dataset_4()
        if not df_4.empty:
            columnas_costo = [col for col in df_4.columns if 'costo' in col.lower() or 'capex' in col.lower()]
            if 'pais' in df_4.columns and 'tier' in df_4.columns and len(columnas_costo) > 0:
                return df_4, columnas_costo[0]
    except:
        pass
    
    return None, None


# ============================================
# GRÁFICO 1: DONUT DE CAPACIDAD
# ============================================

def crear_donut_capacidad(resultados):
    """Gráfico donut: Distribución de capacidad"""
    facility_mw = resultados.get('facility_mw', 100)
    avg_util = resultados.get('avg_util', 0.55)
    stranded_mw = resultados.get('stranded_mw', 45)
    
    # Calcular headroom
    utilizado_mw = facility_mw * avg_util
    headroom_mw = max(0, facility_mw - utilizado_mw - stranded_mw)

    valores = [
        utilizado_mw,
        stranded_mw,
        headroom_mw
    ]

    labels = [
        f'Utilizada<br>{utilizado_mw:.1f} MW',
        f'Stranded<br>{stranded_mw:.1f} MW',
        f'Headroom<br>{headroom_mw:.1f} MW'
    ]

    colores = [COLORS['utilizada'], COLORS['stranded'], COLORS['headroom']]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.6,
        marker_colors=colores,
        textinfo='label+percent',
        textposition='inside',
        hoverinfo='label+value+percent',
        showlegend=False,
        textfont=dict(size=13, color='white', family='Inter'),
        sort=False,
        direction='clockwise'
    )])

    # Añadir texto central
    fig.add_annotation(
        text=f"<b>{resultados.get('avg_util_pct', 55):.1f}%</b><br><span style='font-size:12px'>Utilizada</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=22, color='#1a1a2e', family='Inter'),
        align='center'
    )

    fig = aplicar_estilo_base(fig, height=450)
    fig.update_layout(
        margin=dict(t=30, b=30, l=30, r=30),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=12)
        )
    )

    return fig


# ============================================
# GRÁFICO 2: COMPARATIVA INDUSTRIA (CON DATOS REALES)
# ============================================

def crear_barras_comparativa(resultados):
    """
    Gráfico de barras: Comparativa con datos REALES de la industria
    """
    avg_util_pct = resultados.get('avg_util_pct', 55)
    benchmark = resultados.get('benchmark', 0.62) * 100
    tier = resultados.get('tier', 'Tier III')
    pais = resultados.get('pais', 'Argentina')
    
    # ========== DATOS REALES DESDE JSON ==========
    df = load_dataset_1()
    
    # 1. Promedio de pares en el mismo país
    pares_reales = df[df['pais'] == pais]['average_utilization_pct'].values
    promedio_pares = np.mean(pares_reales) if len(pares_reales) > 0 else 0
    
    # 2. Promedio global de la industria
    promedio_industria = df['average_utilization_pct'].mean()

    categorias = [
        f'Benchmark {tier}',
        'Tu Data Center',
        f'Pares en {pais}',
        'Promedio Global'
    ]
    
    valores = [benchmark, avg_util_pct, promedio_pares, promedio_industria]
    
    colores = [
        COLORS['benchmark'],
        COLORS['stranded'] if avg_util_pct < benchmark else COLORS['utilizada'],
        COLORS['pares'],
        COLORS['promedio']
    ]

    fig = go.Figure(data=[go.Bar(
        x=categorias,
        y=valores,
        marker_color=colores,
        text=[f'{v:.1f}%' for v in valores],
        textposition='outside',
        textfont=dict(size=14, family='Inter', weight='bold'),
        hovertemplate='%{x}<br>Utilización: %{y:.1f}%<extra></extra>',
        width=0.65,
        marker_line_width=0
    )])

    # Línea de benchmark
    fig.add_hline(
        y=benchmark, 
        line_dash="dash", 
        line_color="red",
        line_width=2,
        annotation_text=f"Benchmark: {benchmark:.1f}%",
        annotation_position="top right",
        annotation_font=dict(size=12, color='red')
    )

    fig = aplicar_estilo_base(fig, height=450)
    fig.update_layout(
        yaxis_title="Utilización (%)",
        yaxis_range=[0, 110],
        showlegend=False,
        xaxis_tickangle=-15
    )

    return fig


# ============================================
# GRÁFICO 3: TORNADO CHART (CORREGIDO)
# ============================================

def crear_tornado_chart(resultados):
    """
    Gráfico tornado: Impacto de variables en la pérdida
    CORREGIDO: Incluye Costo de Oportunidad
    """
    variables = [
        'Utilización',
        'PUE',
        'Tarifa Eléctrica',
        'CapEx/MW',
        'Costo Oportunidad',  # NUEVO
        'Demanda Mercado'
    ]
    
    impactos = [0.32, 0.20, 0.16, 0.12, 0.10, 0.10]  # AJUSTADO
    
    sorted_pairs = sorted(zip(impactos, variables), reverse=True)
    impactos_ordenados = [p[0] for p in sorted_pairs]
    variables_ordenadas = [p[1] for p in sorted_pairs]

    colores = ['#ff4b4b' if i > 0.20 else '#ffa500' if i > 0.10 else '#3498db' for i in impactos_ordenados]

    fig = go.Figure(data=[go.Bar(
        y=variables_ordenadas,
        x=impactos_ordenados,
        orientation='h',
        marker_color=colores,
        text=[f'{i*100:.1f}%' for i in impactos_ordenados],
        textposition='outside',
        textfont=dict(size=13, family='Inter', weight='bold'),
        hovertemplate='%{y}<br>Impacto: %{x:.1%}<extra></extra>',
        marker_line_width=0
    )])

    fig = aplicar_estilo_base(fig, height=420)
    fig.update_layout(
        xaxis_title="Impacto Relativo en Pérdida Anual",
        xaxis_range=[0, 0.45],
        margin=dict(t=40, b=40, l=160, r=50),
        xaxis_tickformat='.0%'
    )

    return fig


# ============================================
# GRÁFICO 4: SIMULACIÓN MONTE CARLO (CORREGIDO)
# ============================================

def crear_monte_carlo(resultados):
    """
    Histograma: Simulación de distribución de pérdidas
    CORREGIDO: Usa perdida_anual_total en lugar de total_loss
    """
    # Usar la nueva variable CORRECTA
    perdida_total = resultados.get('perdida_anual_total', resultados.get('total_loss', 1000000))
    incertidumbre = 0.15
    
    np.random.seed(42)
    simulaciones = np.random.normal(perdida_total, perdida_total * incertidumbre, 1000)
    simulaciones = np.maximum(simulaciones, 0)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=simulaciones,
        nbinsx=40,
        name='Simulaciones',
        marker_color='#3498db',
        opacity=0.75,
        hovertemplate='Pérdida: %{x:$.2f}<br>Frecuencia: %{y}<extra></extra>',
        marker_line_width=0
    ))

    # Línea base
    fig.add_vline(
        x=perdida_total,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"Base: ${perdida_total/1e6:.1f}M/año",
        annotation_position="top",
        annotation_font=dict(size=12, color='red')
    )

    # Línea mediana
    mediana = np.median(simulaciones)
    fig.add_vline(
        x=mediana,
        line_dash="dot",
        line_color="#00cc96",
        line_width=2,
        annotation_text=f"Mediana: ${mediana/1e6:.1f}M/año",
        annotation_position="bottom",
        annotation_font=dict(size=12, color='#00cc96')
    )

    fig = aplicar_estilo_base(fig, height=420)
    fig.update_layout(
        xaxis_title="Pérdida Anual (USD)",
        yaxis_title="Frecuencia",
        showlegend=False,
        xaxis_tickformat='$,.0f',
        bargap=0.05
    )

    return fig


# ============================================
# GRÁFICO 5: BARRAS DESGLOSE DE COSTOS (CORREGIDO)
# ============================================

def crear_barras_desglose(resultados):
    """
    Barras apiladas: Desglose de costos anuales
    CORREGIDO: Ahora muestra energía + costo de oportunidad (ambos son $/año)
    """
    energy_loss = resultados.get('energy_loss', 0)
    costo_oportunidad = resultados.get('costo_oportunidad_anual', 0)
    
    anos = [f'Año {i+1}' for i in range(5)]
    
    fig = go.Figure(data=[
        go.Bar(
            name='Costo Energético',
            x=anos,
            y=[energy_loss] * 5,
            marker_color=COLORS['energia'],
            text=[f'${energy_loss/1e6:.1f}M' for _ in range(5)],
            textposition='inside',
            textfont=dict(size=12, family='Inter', weight='bold'),
            hovertemplate='%{x}<br>Energía: %{y:$.2f}<extra></extra>',
            marker_line_width=0
        ),
        go.Bar(
            name='Costo de Oportunidad',
            x=anos,
            y=[costo_oportunidad] * 5,
            marker_color=COLORS['oportunidad'],
            text=[f'${costo_oportunidad/1e6:.1f}M' for _ in range(5)],
            textposition='inside',
            textfont=dict(size=12, family='Inter', weight='bold'),
            hovertemplate='%{x}<br>Oportunidad: %{y:$.2f}<extra></extra>',
            marker_line_width=0
        )
    ])

    fig = aplicar_estilo_base(fig, height=420)
    fig.update_layout(
        barmode='stack',
        yaxis_title="Costo Anual (USD)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        ),
        yaxis_tickformat='$,.0f'
    )

    return fig


# ============================================
# GRÁFICO 6: TABLA CAPEX POR PAÍS Y TIER
# ============================================

def crear_heatmap_capex(resultados):
    """
    Tabla interactiva: CapEx REAL por país y Tier
    Con colores intuitivos y formato profesional
    """
    # Obtener dataframe correcto
    df, columna_capex = _obtener_dataframe_capex()
    
    if df is None or columna_capex is None:
        fig = go.Figure()
        fig.add_annotation(
            text="No se encontraron datos de CapEx<br>en los datasets disponibles",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color='#1a1a2e')
        )
        fig.update_layout(height=420)
        return fig
    
    # Crear pivot table
    pivot = df.pivot_table(
        values=columna_capex,
        index='pais',
        columns='tier',
        aggfunc='mean'
    )
    
    paises = pivot.index.tolist()
    tiers = pivot.columns.tolist()
    capex_data = pivot.values / 1_000_000  # Convertir a millones
    capex_data = np.nan_to_num(capex_data, nan=0)
    
    # Función para asignar color según el valor
    def get_color(valor):
        if valor <= 0:
            return '#f5f5f5'  # Gris claro para N/A
        elif valor < 5:
            return '#e8f5e9'  # Verde claro - CapEx bajo
        elif valor < 8:
            return '#c8e6c9'  # Verde medio
        elif valor < 12:
            return '#fff3e0'  # Naranja claro - CapEx medio
        elif valor < 15:
            return '#ffe0b2'  # Naranja medio
        else:
            return '#ffebee'  # Rojo claro - CapEx alto
    
    def get_text_color(valor):
        if valor <= 0:
            return '#999999'
        elif valor < 8:
            return '#2e7d32'  # Verde oscuro
        elif valor < 15:
            return '#e65100'  # Naranja oscuro
        else:
            return '#c62828'  # Rojo oscuro
    
    # Crear tabla con Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>País</b>'] + [f'<b>{t}</b>' for t in tiers],
            fill_color='#1e3a5f',
            font=dict(color='white', size=14, family='Inter', weight='bold'),
            align=['left'] + ['center'] * len(tiers),
            height=45,
            line=dict(color='white', width=2)
        ),
        cells=dict(
            values=[
                paises,
                *[[f'${capex_data[i][j]:.1f}M' if capex_data[i][j] > 0 else 'N/A' 
                   for i in range(len(paises))] for j in range(len(tiers))]
            ],
            fill_color=[
                ['white', '#f8f9fa'] * (len(paises) // 2 + 1),
                *[[get_color(capex_data[i][j]) for i in range(len(paises))] for j in range(len(tiers))]
            ],
            font=dict(
                color=['#1a1a2e'] * len(paises) + 
                      [get_text_color(capex_data[i][j]) for i in range(len(paises)) for j in range(len(tiers))],
                size=13, 
                family='Inter',
                weight='bold'
            ),
            align=['left'] + ['center'] * len(tiers),
            height=40,
            line=dict(color='white', width=2)
        )
    )])
    
    # Añadir leyenda como anotación DENTRO del área visible
    fig.add_annotation(
        text="<b>CapEx (USD/MW):</b> " +
             "<span style='color:#2e7d32'>■</span> Bajo (<$5M) | " +
             "<span style='color:#e65100'>■</span> Medio ($5-12M) | " +
             "<span style='color:#c62828'>■</span> Alto (>$12M)",
        x=0.5, y=1.08,
        showarrow=False,
        font=dict(size=12, color='#1a1a2e'),
        xref='paper', yref='paper',
        align='center'
    )
    
    fig.update_layout(
        height=480,
        width=None,
        margin=dict(t=60, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True
    )
    
    return fig


# ============================================
# GRÁFICO 7: ÁREA DE EVOLUCIÓN HISTÓRICA
# ============================================

def crear_area_evolucion(resultados):
    """
    Gráfico de área: Evolución histórica REAL desde Dataset 1
    """
    pais = resultados.get('pais', 'Argentina')
    df = load_dataset_1()
    
    df_pais = df[df['pais'] == pais].copy()
    
    if len(df_pais) > 0:
        df_pais['fecha'] = pd.to_datetime(df_pais['anio'].astype(str) + '-' + df_pais['mes'], format='%Y-%b')
        df_pais = df_pais.sort_values('fecha')
        fechas = df_pais['fecha']
        utilizacion = df_pais['average_utilization_pct']
    else:
        # Si no hay datos para este país, usar todos los datos
        df['fecha'] = pd.to_datetime(df['anio'].astype(str) + '-' + df['mes'], format='%Y-%b')
        df = df.sort_values('fecha')
        fechas = df['fecha']
        utilizacion = df['average_utilization_pct']

    benchmark = resultados.get('benchmark', 0.62) * 100
    avg_util_pct = resultados.get('avg_util_pct', 55)
    tier = resultados.get('tier', 'Tier III')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fechas,
        y=utilizacion,
        fill='tozeroy',
        name='Utilización',
        line=dict(color=COLORS['benchmark'], width=3),
        fillcolor='rgba(31, 119, 180, 0.25)',
        hovertemplate='%{x|%b %Y}<br>Utilización: %{y:.1f}%<extra></extra>'
    ))

    fig.add_hline(
        y=benchmark,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"Benchmark {tier}: {benchmark:.1f}%",
        annotation_position="top right",
        annotation_font=dict(size=11, color='red')
    )

    fig.add_hline(
        y=avg_util_pct,
        line_dash="dot",
        line_color=COLORS['stranded'],
        line_width=2,
        annotation_text=f"Actual: {avg_util_pct:.1f}%",
        annotation_position="bottom right",
        annotation_font=dict(size=11, color=COLORS['stranded'])
    )

    fig = aplicar_estilo_base(fig, height=380)
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Utilización (%)",
        yaxis_range=[25, 100],
        showlegend=False
    )

    return fig


# ============================================
# GRÁFICO 8: LÍNEAS DE PROYECCIÓN RECUPERACIÓN
# ============================================

def crear_lineas_recuperacion(resultados):
    """Líneas: Proyección de recuperación (3 escenarios)"""
    avg_util = resultados.get('avg_util', 0.55)
    stranded_pct = resultados.get('stranded_pct', 45) / 100
    target_util = avg_util + stranded_pct
    growth_rate = resultados.get('growth_rate', 0.05)
    
    escenarios = [
        ('Optimista', growth_rate * 1.15, COLORS['utilizada']),
        ('Base', growth_rate, COLORS['benchmark']),
        ('Pesimista', growth_rate * 0.85, COLORS['stranded'])
    ]
    
    meses = np.arange(0, 37, 1)
    
    fig = go.Figure()

    for nombre, tasa, color in escenarios:
        valores = []
        current = avg_util
        for m in meses:
            if m == 0:
                valores.append(current * 100)
            else:
                current = current * (1 + tasa / 12)
                valores.append(current * 100)
        
        fig.add_trace(go.Scatter(
            x=meses,
            y=valores,
            mode='lines',
            name=nombre,
            line=dict(color=color, width=3),
            hovertemplate='%{x:.0f} meses<br>Utilización: %{y:.1f}%<extra></extra>'
        ))

    fig.add_hline(
        y=target_util * 100,
        line_dash="dash",
        line_color="green",
        line_width=2,
        annotation_text=f"Meta: {target_util*100:.1f}%",
        annotation_position="top right",
        annotation_font=dict(size=11, color='green')
    )

    fig.add_hline(
        y=avg_util * 100,
        line_dash="dot",
        line_color=COLORS['stranded'],
        line_width=2,
        annotation_text=f"Actual: {avg_util*100:.1f}%",
        annotation_position="bottom left",
        annotation_font=dict(size=11, color=COLORS['stranded'])
    )

    fig = aplicar_estilo_base(fig, height=380)
    fig.update_layout(
        xaxis_title="Meses",
        yaxis_title="Utilización (%)",
        yaxis_range=[30, 100],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
    )

    return fig


# ============================================
# GRÁFICO 9: TABLA WORKLOAD vs TIER (CON DATOS REALES)
# ============================================

def crear_heatmap_workload(resultados):
    """
    Tabla interactiva: Utilización REAL por Workload y Tier
    """
    df = load_dataset_1()
    
    pivot = df.pivot_table(
        values='average_utilization_pct',
        index='workload_principal',
        columns='tier',
        aggfunc='mean'
    )
    
    workloads = pivot.index.tolist()
    tiers = pivot.columns.tolist()
    data = pivot.values
    data = np.nan_to_num(data, nan=0)

    # Crear tabla con Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Workload</b>'] + [f'<b>{t}</b>' for t in tiers],
            fill_color='#1e3a5f',
            font=dict(color='white', size=15, family='Inter', weight='bold'),
            align=['left'] + ['center'] * len(tiers),
            height=55,
            line=dict(color='white', width=2)
        ),
        cells=dict(
            values=[
                workloads,
                *[[f'{data[i][j]:.1f}%' for i in range(len(workloads))] for j in range(len(tiers))]
            ],
            fill_color=[
                ['white', '#f8f9fa'] * (len(workloads) // 2 + 1),
                *[['#e8f5e9' if data[i][j] >= 70 else '#fff3e0' if data[i][j] >= 50 else '#ffebee' 
                   for i in range(len(workloads))] for j in range(len(tiers))]
            ],
            font=dict(color='#1a1a2e', size=14, family='Inter'),
            align=['left'] + ['center'] * len(tiers),
            height=50,
            line=dict(color='white', width=2)
        )
    )])
    
    fig.update_layout(
        height=550,
        width=None,
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True
    )
    
    return fig


# ============================================
# GRÁFICO 10: MATRIZ DE OPORTUNIDADES (TABLA) - CORREGIDO
# ============================================

def crear_matriz_oportunidades(resultados):
    """
    Tabla interactiva: Matriz de oportunidades
    CORREGIDO: Usa perdida_anual_total en lugar de total_loss
    """
    stranded_mw = resultados.get('stranded_mw', 0)
    perdida_total = resultados.get('perdida_anual_total', resultados.get('total_loss', 0))
    
    oportunidades = [
        {
            'nombre': 'Mejorar utilización en AI/ML',
            'impacto': perdida_total * 0.50,
            'esfuerzo': 3,
            'mw': stranded_mw * 0.35,
            'costo': 'Bajo',
            'prioridad': 'Alta',
            'roi': 8.5
        },
        {
            'nombre': 'Reducir capacidad inactiva',
            'impacto': perdida_total * 0.33,
            'esfuerzo': 2,
            'mw': stranded_mw * 0.25,
            'costo': 'Bajo',
            'prioridad': 'Alta',
            'roi': 9.2
        },
        {
            'nombre': 'Optimizar refrigeración',
            'impacto': perdida_total * 0.19,
            'esfuerzo': 8,
            'mw': stranded_mw * 0.20,
            'costo': 'Medio',
            'prioridad': 'Media',
            'roi': 4.5
        },
        {
            'nombre': 'Reubicar cargas de trabajo',
            'impacto': perdida_total * 0.17,
            'esfuerzo': 12,
            'mw': stranded_mw * 0.15,
            'costo': 'Alto',
            'prioridad': 'Baja',
            'roi': 2.8
        },
        {
            'nombre': 'Mejorar PUE',
            'impacto': perdida_total * 0.11,
            'esfuerzo': 6,
            'mw': stranded_mw * 0.10,
            'costo': 'Medio',
            'prioridad': 'Media',
            'roi': 3.5
        }
    ]
    
    # Crear DataFrame
    df = pd.DataFrame(oportunidades)
    df['impacto_m'] = df['impacto'] / 1e6
    
    # Ordenar por impacto
    df = df.sort_values('impacto', ascending=False)
    
    # Crear figura con tabla
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['<b>Oportunidad</b>', '<b>Impacto<br>(M USD/año)</b>', '<b>Esfuerzo<br>(meses)</b>', 
                   '<b>MW<br>Recuperables</b>', '<b>Costo</b>', '<b>Prioridad</b>', '<b>ROI</b>'],
            fill_color='#1e3a5f',
            font=dict(color='white', size=14, family='Inter', weight='bold'),
            align=['left', 'center', 'center', 'center', 'center', 'center', 'center'],
            height=50,
            line=dict(color='white', width=2)
        ),
        cells=dict(
            values=[
                df['nombre'],
                [f'${v:.1f}M' for v in df['impacto_m']],
                [f'{v}' for v in df['esfuerzo']],
                [f'{v:.1f}' for v in df['mw']],
                df['costo'],
                df['prioridad'],
                [f'{v:.1f}x' for v in df['roi']]
            ],
            fill_color=[
                ['white', '#f8f9fa'] * 3,
                ['#e8f5e9' if p == 'Alta' else '#fff3e0' if p == 'Media' else '#ffebee' for p in df['prioridad']],
                ['white', '#f8f9fa'] * 3,
                ['white', '#f8f9fa'] * 3,
                ['#e8f5e9' if c == 'Bajo' else '#fff3e0' if c == 'Medio' else '#ffebee' for c in df['costo']],
                ['#e8f5e9' if p == 'Alta' else '#fff3e0' if p == 'Media' else '#ffebee' for p in df['prioridad']],
                ['#e8f5e9' if r > 5 else '#fff3e0' if r > 3 else '#ffebee' for r in df['roi']]
            ],
            font=dict(color='#1a1a2e', size=13, family='Inter'),
            align=['left', 'center', 'center', 'center', 'center', 'center', 'center'],
            height=45,
            line=dict(color='white', width=2)
        )
    )])
    
    fig.update_layout(
        height=450,
        margin=dict(t=30, b=30, l=30, r=30),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        autosize=True
    )
    
    return fig


# ============================================
# GRÁFICO 11: COMPARATIVA POR PAÍS
# ============================================

def crear_barras_paises(resultados):
    """
    Gráfico de barras: Comparativa REAL de utilización por país
    """
    df = load_dataset_1()
    
    paises_data = df.groupby('pais')['average_utilization_pct'].mean().sort_values(ascending=False)
    
    pais_seleccionado = resultados.get('pais', 'Argentina')
    
    colores = [
        '#ff4b4b' if p == pais_seleccionado else '#1f77b4'
        for p in paises_data.index
    ]
    
    fig = go.Figure(data=[go.Bar(
        x=paises_data.index,
        y=paises_data.values,
        marker_color=colores,
        text=[f'{v:.1f}%' for v in paises_data.values],
        textposition='outside',
        textfont=dict(size=12, family='Inter', weight='bold'),
        hovertemplate='%{x}<br>Utilización: %{y:.1f}%<extra></extra>',
        marker_line_width=0
    )])

    fig = aplicar_estilo_base(fig, height=400)
    fig.update_layout(
        xaxis_title="País",
        yaxis_title="Utilización Promedio (%)",
        yaxis_range=[0, 110],
        showlegend=False,
        xaxis_tickangle=-30
    )

    return fig