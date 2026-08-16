"""
Banner dinámico con Font Awesome y animaciones
Colores cambian según la magnitud de stranded capacity
"""

import streamlit as st

def mostrar_banner(resultados):
    """
    Muestra el banner dinámico según los resultados
    """
    
    stranded_pct = resultados.get('stranded_pct', 0)
    stranded_mw = resultados.get('stranded_mw', 0)
    perdida_anual = resultados.get('perdida_anual', 0)
    recovery_time = resultados.get('recovery_time', 0)
    avg_util_pct = resultados.get('avg_utilization', resultados.get('avg_util_pct', 55))
    benchmark = resultados.get('benchmark_avg', 62)
    benchmark_diff = resultados.get('benchmark_diff', 0)
    tier = resultados.get('tier', 'Tier III')
    pais = resultados.get('pais', '')
    growth_rate = resultados.get('growth_rate', 0.05)
    pue = resultados.get('pue', 1.5)
    
    # ============================================
    # 7 NIVELES DE SEVERIDAD CON COLORES DISTINTOS
    # ============================================
    
    if stranded_pct >= 40:
        icono = 'fa-skull-crossbones'
        titulo = '🚨 PELIGRO CRÍTICO: CAPACIDAD MASIVAMENTE STRANDED'
        color_borde = '#ff0000'
        color_fondo = 'linear-gradient(135deg, #450a0a 0%, #dc2626 30%, #7f1d1d 60%, #450a0a 100%)'
        color_acento = '#ff6b6b'
        animacion = 'pulse 1.5s infinite'
        severidad = 'EXTREMA'
    elif stranded_pct >= 30:
        icono = 'fa-circle-exclamation'
        titulo = '🔴 ALERTA CRÍTICA DE CAPACIDAD STRANDED'
        color_borde = '#ff4b4b'
        color_fondo = 'linear-gradient(135deg, #7f1d1d 0%, #dc2626 50%, #991b1b 100%)'
        color_acento = '#ff4b4b'
        animacion = 'pulse 2s infinite'
        severidad = 'CRÍTICA'
    elif stranded_pct >= 25:
        icono = 'fa-triangle-exclamation'
        titulo = '🟠 ADVERTENCIA ALTA DE CAPACIDAD STRANDED'
        color_borde = '#ff8c00'
        color_fondo = 'linear-gradient(135deg, #7c2d12 0%, #ea580c 50%, #9a3412 100%)'
        color_acento = '#ffa500'
        animacion = 'shake 0.8s infinite'
        severidad = 'ALTA'
    elif stranded_pct >= 20:
        icono = 'fa-triangle-exclamation'
        titulo = '⚠️ ADVERTENCIA DE CAPACIDAD STRANDED'
        color_borde = '#ffa500'
        color_fondo = 'linear-gradient(135deg, #1e3a5f 0%, #2d4a7a 50%, #1e3a5f 100%)'
        color_acento = '#ffa500'
        animacion = 'shake 1s infinite'
        severidad = 'MEDIA-ALTA'
    elif stranded_pct >= 15:
        icono = 'fa-exclamation'
        titulo = '🟡 PRECAUCIÓN: CAPACIDAD SUBUTILIZADA'
        color_borde = '#f59e0b'
        color_fondo = 'linear-gradient(135deg, #1e3a5f 0%, #3b5998 50%, #2d4a7a 100%)'
        color_acento = '#fbbf24'
        animacion = 'none'
        severidad = 'MEDIA'
    elif stranded_pct >= 10:
        icono = 'fa-info-circle'
        titulo = '🔵 CAPACIDAD LIGERAMENTE SUBUTILIZADA'
        color_borde = '#60a5fa'
        color_fondo = 'linear-gradient(135deg, #1e3a5f 0%, #2563eb 50%, #1e40af 100%)'
        color_acento = '#93c5fd'
        animacion = 'none'
        severidad = 'LEVE'
    else:
        icono = 'fa-circle-check'
        titulo = '✅ CAPACIDAD SALUDABLE'
        color_borde = '#00cc96'
        color_fondo = 'linear-gradient(135deg, #064e3b 0%, #059669 50%, #047857 100%)'
        color_acento = '#34d399'
        animacion = 'none'
        severidad = 'ÓPTIMA'
    
    perdida_diaria = perdida_anual / 365
    
    banner_html = f"""
    <style>
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 {color_borde}80; }}
            70% {{ box-shadow: 0 0 0 20px {color_borde}00; }}
            100% {{ box-shadow: 0 0 0 0 {color_borde}80; }}
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-3px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(3px); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(-30px) scale(0.95); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -200% center; }}
            100% {{ background-position: 200% center; }}
        }}
        
        @keyframes barFill {{
            from {{ width: 0%; }}
            to {{ width: {stranded_pct}%; }}
        }}
        
        @keyframes iconBounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-8px); }}
        }}
        
        @keyframes glow {{
            0%, 100% {{ text-shadow: 0 0 10px {color_acento}, 0 0 20px {color_acento}; }}
            50% {{ text-shadow: 0 0 20px {color_acento}, 0 0 40px {color_acento}; }}
        }}
        
        .banner-dynamic {{
            background: {color_fondo};
            border-radius: 18px;
            padding: 24px 30px;
            margin-bottom: 25px;
            color: white;
            border-left: 8px solid {color_borde};
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
            animation: slideIn 0.6s ease-out, {animacion};
            position: relative;
            overflow: hidden;
        }}
        
        .banner-dynamic::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 4px;
            background: linear-gradient(90deg, transparent, {color_acento}, transparent);
            animation: shimmer 2.5s linear infinite;
            background-size: 200% auto;
        }}
        
        .banner-dynamic .banner-title {{
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 14px;
            letter-spacing: 0.5px;
            animation: glow 2s ease-in-out infinite;
        }}
        
        .banner-dynamic .banner-title i {{
            font-size: 28px;
            color: {color_acento};
            animation: iconBounce 2s ease-in-out infinite;
            filter: drop-shadow(0 0 12px {color_acento});
        }}
        
        .banner-dynamic .severidad-badge {{
            display: inline-block;
            background: {color_borde}30;
            border: 1px solid {color_borde};
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        
        .banner-dynamic .banner-subtitle {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 14px;
        }}
        
        .banner-dynamic .banner-stats {{
            display: flex;
            gap: 12px;
            margin: 12px 0;
            flex-wrap: wrap;
        }}
        
        .banner-dynamic .banner-stat {{
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 24px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}
        
        .banner-dynamic .banner-stat:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
        }}
        
        .banner-dynamic .banner-stat i {{
            color: {color_acento};
        }}
        
        .banner-dynamic .banner-stat .valor {{
            font-weight: 800;
            font-size: 14px;
        }}
        
        .banner-dynamic .banner-bar {{
            width: 100%;
            height: 10px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            margin-top: 14px;
            overflow: hidden;
        }}
        
        .banner-dynamic .banner-bar-fill {{
            height: 100%;
            border-radius: 8px;
            background: linear-gradient(90deg, {color_borde}, {color_acento}, #a78bfa, {color_acento}, {color_borde});
            animation: barFill 1.5s ease-out, shimmer 2s linear infinite;
            background-size: 300% auto;
            transition: width 0.5s ease;
        }}
        
        .banner-dynamic .banner-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            opacity: 0.75;
            margin-top: 10px;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .banner-dynamic .banner-footer i {{
            color: {color_acento};
        }}
    </style>
    
    <div class="banner-dynamic">
        <div class="banner-title">
            <i class="fa-solid {icono}"></i>
            <div>
                {titulo}
                <div style="margin-top: 4px;">
                    <span class="severidad-badge">Severidad: {severidad}</span>
                </div>
            </div>
        </div>
        
        <div class="banner-subtitle">
            <i class="fa-solid fa-location-dot" style="color: #60a5fa;"></i> 
            <strong>{pais}</strong> · {tier} · 
            Tu data center tiene <strong style="color: {color_acento}; font-size: 16px;">{stranded_mw:.1f} MW</strong> sin utilizar 
            (<strong style="color: {color_acento};">{stranded_pct:.1f}%</strong> de tu capacidad total)
        </div>
        
        <div class="banner-stats">
            <span class="banner-stat">
                <i class="fa-solid fa-sack-dollar"></i> 
                <span class="valor">${perdida_anual:.1f} M</span> pérdida anual
            </span>
            <span class="banner-stat">
                <i class="fa-solid fa-clock"></i> 
                <span class="valor">{recovery_time} años</span> recuperación
            </span>
            <span class="banner-stat">
                <i class="fa-solid fa-chart-simple"></i> 
                <span class="valor">{benchmark_diff:+.1f}%</span> vs benchmark
            </span>
            <span class="banner-stat">
                <i class="fa-solid fa-gauge-high"></i> 
                Utilización: <span class="valor">{avg_util_pct:.1f}%</span>
            </span>
            <span class="banner-stat">
                <i class="fa-solid fa-bolt"></i> 
                PUE: <span class="valor">{pue:.2f}</span>
            </span>
        </div>
        
        <div class="banner-bar">
            <div class="banner-bar-fill" style="width: {stranded_pct}%;"></div>
        </div>
        
        <div class="banner-footer">
            <span><i class="fa-solid fa-chart-line"></i> Utilización: {avg_util_pct:.1f}%</span>
            <span><i class="fa-solid fa-target"></i> Benchmark {tier}: {benchmark:.1f}%</span>
            <span><i class="fa-solid fa-arrow-trend-up"></i> Growth: {growth_rate*100:.1f}% YoY</span>
            <span><i class="fa-solid fa-dollar-sign"></i> Pérdida diaria: ${perdida_diaria:.2f} M</span>
        </div>
    </div>
    """
    
    st.markdown(banner_html, unsafe_allow_html=True)