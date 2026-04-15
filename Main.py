import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTO NIVEL - ESTÁNDAR NASA/ORIÓN
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# CSS: ESTÉTICA CIRCULAR DE GRADO AEROESPACIAL
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');
    
    /* Fondo Gris Claro de Instrumentación */
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Roboto Mono', monospace; }
    
    /* Título Monolineal Superior */
    h1 { color: #0D47A1 !important; text-transform: uppercase; font-size: 1.8em !important; text-align: center; border-bottom: 2px solid #0D47A1; padding-bottom: 10px; margin-bottom: 20px !important; }
    
    /* UNIFORMIDAD CIRCULAR (Contenedores) */
    .circular-container {
        background-color: #FFFFFF;
        border: 2px solid #BDBDBD;
        border-radius: 50%; /* FORMA CIRCULAR PERFECTA */
        width: 320px;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin: 10px auto;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.15);
        color: #1A1A1A;
        padding: 20px;
    }
    
    /* Alarma de Perforación Circular (Roja pulsante) */
    @keyframes breathing {
      0% { border-color: #F44336; box-shadow: 0 0 5px #F44336; }
      50% { border-color: #B71C1C; box-shadow: 0 0 20px #F44336; }
      100% { border-color: #F44336; box-shadow: 0 0 5px #F44336; }
    }
    .circular-alarm {
        border: 4px solid #F44336;
        animation: breathing 1.5s infinite ease-in-out;
        background-color: #FFCDD2;
        color: #B71C1C;
    }
    
    h3 { color: #0D47A1 !important; text-transform: uppercase; font-size: 1.1em; margin-bottom: 15px; }
    .stMetric { background-color: rgba(0,0,0,0) !important; border: none !important; }
    .stMetric label { color: #666 !important; }
    .stMetric .st-c3 { color: #0D47A1 !important; font-size: 2em; font-weight: bold; }
    
    /* Limpieza de Sidebar */
    .sidebar .sidebar-content { background-color: #F5F5F5; }
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

# --- MAIN INTERFACE: MONOLINEAR TITLE ---
st.markdown("<h1>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1.5, 1])

with col1:
    # CÍRCULO 1: TARGET COORDINATES (UNIFICADO)
    st.markdown(f"""
    <div class="circular-container">
        <h3>📍 TARGET COORDINATES</h3>
        <p><strong>LATITUDE:</strong><br><span style="color: #0D47A1; font-size: 1.2em;">{4.71 + (v1/1000):.4f}</span></p>
        <p><strong>LONGITUDE:</strong><br><span style="color: #0D47A1; font-size: 1.2em;">{-74.07 + (v2/1000):.4f}</span></p>
        <p><strong>REF-DEPTH:</strong><br><span style="color: #0D47A1; font-size: 1.4em; font-weight:bold;">{depth:.1f} m</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # CÍRCULO 2: STREAM VARIATION (UNIFICADO)
    st.markdown('<div class="circular-container" style="height: 280px; width: 280px;"><h3>STREAM VARIATION</h3>', unsafe_allow_html=True)
    flow_stability = np.random.randn(20) * (v4 / 15)
    st.line_chart(flow_stability, height=180)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # ESFERA AZUL CIELO CON REJILLA PERMANENTE Y DIAMANTE CONTENIDO
    dx, dy = v1/500, v2/500
    # Límite matemático estricto para que el diamante NO salga de la esfera
    dz = np.clip(0.8 + (v6/400), 0.0, 0.95)

    fig = go.Figure()
    # Tierra Azul Cielo con líneas de rejilla VISIBLES permanentemente
    phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.6, 
                             colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
                             contours=dict(x=dict(show=True, color="white", width=1),
                                           y=dict(show=True, color="white", width=1),
                                           z=dict(show=True, color="white", width=1))))
    
    # Diamante (Core Point) - Contenido
    fig.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                               marker=dict(size=18, color='#00FF00', symbol='diamond', line=dict(color='black', width=2))))

    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=650,
        modebar=dict(bgcolor='white', color='black')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

with col3:
    # CÍRCULO 3: SYSTEM ANALYTICS (UNIFICADO, FONDO BLANCO, SIN ESCUDO)
    
    # Lógica de Alarma Circular
    alarm_class = "circular-alarm" if sync_score > 75 else ""
    status_text = "DRILLING POINT CONFIRMED" if sync_score > 75 else "SCANNING SUBSURFACE..."
    
    st.markdown(f"""
    <div class="circular-container {alarm_class}">
        <h3>🛡️ SYSTEM ANALYTICS</h3>
        <p style="font-size: 0.9em; font-weight: bold; margin-bottom: 15px;">{status_text}</p>
        <span style="color: #666; font-size: 0.9em;">SYNC-COHERENCE INDEX:</span><br>
        <span style="font-size: 2.2em; font-weight: bold; color: #0D47A1;">{sync_score:.2f}%</span><br>
        <hr style="margin: 15px 0; border: 0; border-top: 1px solid #BDBDBD; width: 80%;">
        <span style="color: #666; font-size: 0.9em;">MASS STABILITY:</span><br>
        <span style="color: #1A1A1A; font-weight: bold;">{v5:.2f} R-MASS</span>
    </div>
    """, unsafe_allow_html=True)
    
    # CÍRCULO 4: SPIDER CHART (AGRANDADO PARA ARMONÍA)
    st.markdown('<div class="circular-container" style="height: 380px; width: 380px; padding: 10px;">', unsafe_allow_html=True)
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[abs(v1/5), abs(v2/5), v3/9, v4*10, v5*20, v6*2],
        theta=categories, fill='toself', fillcolor='rgba(0, 191, 255, 0.5)',
        line=dict(color='#0D47A1', width=2)
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="#E1F5FE", radialaxis=dict(visible=True, gridcolor="white", tickfont=dict(color="#0D47A1"))),
        paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=360, margin=dict(l=30, r=30, b=30, t=30)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #999; font-size: 0.7em; margin-top: 20px;'>NASA-STD INSTRUMENTATION | MISSION CONTROL CONFIGURATION | CONFIDENTIAL PROPERTY DR. ESPÍNDOLA NIÑO</div>", unsafe_allow_html=True)