import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTO NIVEL - NASA STYLE
st.set_page_config(page_title="SINCRO+ X | PROTOTYPE", layout="wide")

# CSS: ESTÉTICA DE INSTRUMENTACIÓN CLARA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Roboto Mono', monospace; }
    
    /* Cajas Blancas de Información */
    .info-box {
        background-color: #FFFFFF;
        border: 1px solid #BDBDBD;
        padding: 15px;
        border-radius: 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: #1A1A1A;
        margin-bottom: 10px;
    }
    
    /* Alarma de Perforación (Roja que respira) */
    @keyframes breathing {
      0% { background-color: #FFCDD2; }
      50% { background-color: #F44336; }
      100% { background-color: #FFCDD2; }
    }
    .alarm-active {
        animation: breathing 2s infinite ease-in-out;
        padding: 15px;
        border-radius: 4px;
        text-align: center;
        font-weight: bold;
        color: white;
        border: 1px solid #B71C1C;
    }
    
    h1, h2, h3 { color: #0D47A1 !important; text-transform: uppercase; }
    .stMetric { background-color: #FFFFFF !important; border: 1px solid #BDBDBD !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SUBSYSTEM CALIBRATION ---
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM CALIBRATION")
    v1 = st.slider("V-TENSOR [G-01]", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX RES", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL EXC", 300, 900, 450)
    v4 = st.slider("C-MATRIX SYNC", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS DENSITY", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR INDEX", 0.0, 40.0, 15.0)

# Lógica de Datos
depth = (v3 / 5) + (v5 * 100)
sync_score = (v4 * 8) + (v6 / 2)

# --- MAIN INTERFACE ---
st.markdown("<h1>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("### 📍 TARGET COORDINATES")
    st.markdown(f"""
    <div class="info-box">
        <strong>LATITUDE:</strong> {4.71 + (v1/1000):.4f}<br>
        <strong>LONGITUDE:</strong> {-74.07 + (v2/1000):.4f}<br>
        <strong>REF-DEPTH:</strong> {depth:.1f} m
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### STREAM VARIATION")
    flow_stability = np.random.randn(20) * (v4 / 15)
    st.line_chart(flow_stability, height=200)

with col2:
    # ESFERA AZUL CIELO
    dx, dy = v1/500, v2/500
    dz = np.clip(0.8 + (v6/400), 0.0, 0.95)

    fig = go.Figure()
    # Tierra Azul Cielo
    phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.5, 
                             colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False))
    
    # Diamante (Core Point)
    fig.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                               marker=dict(size=15, color='#00FF00', symbol='diamond', line=dict(color='black', width=2))))

    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=550,
        modebar=dict(bgcolor='white', color='black')
    )
    st.plotly_chart(fig, use_container_width=True)

with col3:
    st.markdown("### 🛡️ SYSTEM ANALYTICS")
    
    if sync_score > 75:
        st.markdown('<div class="alarm-active">DRILLING POINT CONFIRMED</div>', unsafe_allow_html=True)
    else:
        st.warning("SCANNING SUBSURFACE...")

    # Caja Blanca de Datos Analíticos
    st.markdown(f"""
    <div class="info-box">
        <span style="color: #666;">SYNC-COHERENCE INDEX:</span><br>
        <span style="font-size: 24px; font-weight: bold; color: #0D47A1;">{sync_score:.2f}%</span><br>
        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #EEE;">
        <span style="color: #666;">MASS STABILITY:</span> {v5:.2f} R-MASS
    </div>
    """, unsafe_allow_html=True)
    
    # Spider Chart (Fondo Azul Cielo)
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[abs(v1/5), abs(v2/5), v3/9, v4*10, v5*20, v6*2],
        theta=categories, fill='toself', fillcolor='rgba(0, 191, 255, 0.5)',
        line=dict(color='#0D47A1', width=2)
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="#E1F5FE", radialaxis=dict(visible=True, gridcolor="white")),
        paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=300
    )
    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("<div style='text-align: center; color: #999; font-size: 0.7em;'>NASA-STD INSTRUMENTATION | CONFIDENTIAL PROPERTY DR. ESPÍNDOLA NIÑO</div>", unsafe_allow_html=True)