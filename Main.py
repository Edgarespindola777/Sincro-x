import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTA SEGURIDAD
st.set_page_config(page_title="SINCRO-X | MISSION CONTROL", layout="wide")

# CSS: ESTÉTICA NASA CON EFECTO DE RESPIRACIÓN ROJA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'JetBrains Mono', monospace; }
    
    /* Efecto Respiración para Alarma Roja */
    @keyframes breathing {
      0% { background-color: #440000; box-shadow: 0 0 5px #ff0000; }
      50% { background-color: #ff0000; box-shadow: 0 0 25px #ff0000; }
      100% { background-color: #440000; box-shadow: 0 0 5px #ff0000; }
    }
    .alarm-active {
        animation: breathing 1.5s infinite ease-in-out;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        color: white;
        border: 2px solid #ff4444;
    }
    .stMetric { background: #1A1A1A; border: 1px solid #444; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL DE SENSORES CIFRADOS (PROTECCIÓN DE IDEA) ---
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM CALIBRATION")
    v1 = st.slider("V-TENSOR [G-01]", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX RES", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL EXC", 300, 900, 450)
    v4 = st.slider("C-MATRIX SYNC", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS DENSITY", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR INDEX", 0.0, 40.0, 15.0)

# --- LÓGICA DE DETECCIÓN ---
depth = (v3 / 5) + (v5 * 100)
sync_score = (v4 * 8) + (v6 / 2)

# --- CUERPO PRINCIPAL ---
st.markdown("<h1 style='color: #00E5FF; letter-spacing: 3px;'>SINCRO-X | ANALÍTICA GEODÉSICA</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 📊 TELEMETRÍA")
    st.code(f"COORDINATE-X: {4.71 + (v1/1000):.4f}\nCOORDINATE-Y: {-74.07 + (v2/1000):.4f}\nREF-DEPTH: {depth:.1f}m", language="bash")
    
    st.write("VARIACIONES DE FLUJO (ESTABILIDAD)")
    flow_data = pd.DataFrame(np.random.randn(20, 1), columns=['V-STREAM'])
    st.line_chart(flow_data, height=150)

with col2:
    # ESFERA AZUL CLARO CON DIAMANTE DINÁMICO
    dx = (v1/500)
    dy = (v2/500)
    dz = 0.8 + (v6/400)

    fig = go.Figure()
    
    # Capa de la Tierra Azul Claro Traslúcida
    phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    x = np.cos(phi)*np.sin(theta)
    y = np.sin(phi)*np.sin(theta)
    z = np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.4, colorscale=[[0, '#00D2FF'], [1, '#3a7bd5']], showscale=False))
    
    # Objetivo Diamante Verde
    fig.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                               marker=dict(size=18, color='#00FF00', symbol='diamond', line=dict(color='white', width=3))))

    # Configuración de visibilidad total de controles
    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        paper_bgcolor='black', margin=dict(l=0,r=0,b=0,t=0), height=550,
        modebar=dict(bgcolor='rgba(255,255,255,0.2)', color='white', activecolor='#00FF00')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

with col3:
    st.markdown("### ⚡ ANALÍTICA")
    # Indicador de Perforación con efecto de respiración
    if sync_score > 72:
        st.markdown('<div class="alarm-active">PUNTO DE PERFORACIÓN CONFIRMADO</div>', unsafe_allow_html=True)
    else:
        st.info("SISTEMA EN BÚSQUEDA...")

    st.metric("COHERENCIA MATRICIAL", f"{sync_score:.1f}%", delta=f"{v5:.1f} R-MASS")
    
    # Firma Geofísica (Radar de alto contraste)
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[abs(v1/5), abs(v2/5), v3/9, v4*10, v5*20, v6*2],
        theta=categories, fill='toself', fillcolor='rgba(0, 255, 0, 0.3)',
        line=dict(color='#00FF00', width=2)
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="#222222", radialaxis=dict(visible=True, gridcolor="#444", tickfont=dict(color="white"))), 
        paper_bgcolor='black', font=dict(color="white"), showlegend=False, height=350
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.write("---")
st.caption("LOGOS PREDICTIVE ENGINE V.4.0 | PI: DR. ESPÍNDOLA NIÑO | CONFIDENTIAL ACCESS")