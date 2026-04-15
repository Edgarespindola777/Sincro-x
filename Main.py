import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE INTERFAZ PROFESIONAL
st.set_page_config(page_title="SINCRO-X | MISSION CONTROL", layout="wide")

# CSS: ESTÉTICA DE INSTRUMENTACIÓN CIENTÍFICA (NASA STYLE)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;500&display=swap');
    .stApp { background-color: #050505; color: #D1D1D1; font-family: 'JetBrains Mono', monospace; }
    .stMetric { background: #0a0a0a; border-left: 3px solid #4CAF50; padding: 10px; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 300; letter-spacing: 2px; border-bottom: 1px solid #333; }
    .sidebar .sidebar-content { background-color: #0a0a0a; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CONTROLADORES (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🛰️ SUBSYSTEMS INPUT")
    st.write("MATRIX CALIBRATION")
    
    # SENSORES UNIFICADOS
    v1 = st.slider("GRAVIMETRÍA (DTGQ)", -500.0, 500.0, -112.0)
    v2 = st.slider("MAGNETOMETRÍA (V-RES)", 0.0, 100.0, 45.0)
    v3 = st.slider("EXCITACIÓN TÉRMICA (K)", 273, 800, 394)
    v4 = st.slider("RESONANCIA CRISTALINA", 1.0, 5.0, 2.85)
    v5 = st.slider("DENSIDAD DE MATRIZ (g/cm³)", 1.5, 4.5, 2.67)
    v6 = st.slider("POROSIDAD ESTRUCTURAL (%)", 0.0, 30.0, 12.5)
    
    st.write("---")
    status = st.select_slider("SYSTEM STATUS", ["STANDBY", "SYNCING", "LOCKED"], value="SYNCING")

# --- CUERPO PRINCIPAL ---
st.markdown("# SINCRO-X | ANALÍTICA DE BASAMENTO CRISTALINO")
st.caption(f"COORDENADAS DE PROSPECCIÓN CUÁNTICA | {time.strftime('%H:%M:%S')} UTC")

col_left, col_mid, col_right = st.columns([1, 2, 1])

# COLUMNA IZQUIERDA: TELEMETRÍA NUMÉRICA
with col_left:
    st.markdown("### 📊 DATA STREAM")
    # Simulación de coordenadas dinámicas basadas en los sliders
    lat_target = 4.7110 + (v1 / 10000)
    lon_target = -74.0721 + (v2 / 10000)
    depth_calc = (v3 / 10) + (v5 * 10)
    
    st.code(f"TARGET_LAT: {lat_target:.6f}\nTARGET_LON: {lon_target:.6f}\nDEPTH_REF: {depth_calc:.2f}m", language="bash")
    
    st.write("VARIACIÓN DE FLUJO")
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=['SYNC'])
    st.line_chart(chart_data, height=150)

# COLUMNA CENTRAL: TIERRA 3D Y DIAMANTE DINÁMICO
with col_mid:
    # Lógica de posición del diamante (Triangulación)
    # El diamante se mueve en X, Y por gravimetría/magnetometría y en Z por densidad/porosidad
    dx = np.cos(v1/100) * 0.8
    dy = np.sin(v2/10) * 0.8
    dz = 0.5 + (v6/60) # Sube o baja según porosidad
    
    # Esfera Terrestre (Estilo Wireframe NASA)
    phi = np.linspace(0, 2*np.pi, 60)
    theta = np.linspace(0, np.pi, 60)
    x = np.outer(np.cos(phi), np.sin(theta))
    y = np.outer(np.sin(phi), np.sin(theta))
    z = np.outer(np.ones(np.size(phi)), np.cos(theta))

    fig = go.Figure()

    # Superficie de la Tierra (Sutil)
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.15, colorscale='Greys', showscale=False))

    # Diamante de Objetivo (DINÁMICO)
    fig.add_trace(go.Scatter3d(
        x=[dx], y=[dy], z=[dz],
        mode='markers+text',
        name='TARGET',
        marker=dict(size=12, color='#4CAF50', symbol='diamond', line=dict(color='white', width=2)),
        text=[f"POINT ALPHA: {depth_calc:.1f}m"],
        textposition="top center"
    ))

    # Configuración de Cámara y Estilo
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True}) # Mantiene visibles los controles

# COLUMNA DERECHA: RESULTADOS CUÁNTICOS
with col_right:
    st.markdown("### ⚡ ANALÍTICA")
    # El índice de sincronía ahora depende de la densidad y resonancia
    sync_idx = (v4 * 15) + (v5 * 5)
    st.metric("ÍNDICE DE SINCRONÍA", f"{sync_idx:.2f}%", delta=f"{v6/10:.1f} структур")
    
    # Firma de Resonancia (Radar)
    categories = ['Grav', 'Mag', 'Temp', 'Res', 'Dens', 'Poro']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[abs(v1/5), v2, v3/8, v4*20, v5*20, v6*3],
        theta=categories,
        fill='toself',
        line=dict(color='#4CAF50')
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="#0a0a0a"),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, b=40, t=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.write("---")
st.markdown(f"<div style='text-align: center; color: #444;'>LOGOS PREDICTIVE ENGINE V.4.0 | PI: DR. ESPÍNDOLA NIÑO | SECURE ACCESS TERMINAL</div>", unsafe_allow_html=True)