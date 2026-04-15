import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTA PRECISIÓN - NASA STD
st.set_page_config(page_title="SINCRO+ X | PROTOTYPE", layout="wide")

# CSS: ESTÉTICA DE INSTRUMENTACIÓN CIENTÍFICA (HIGH-LEGIBILITY)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Fondo Gris Aeroespacial Ligero */
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Courier New', monospace; }
    
    /* Título Monolineal Superior Sobrio */
    h1 { 
        color: #0D47A1 !important; text-transform: uppercase; font-size: 1.8em !important; 
        text-align: center; border-bottom: 2px solid #0D47A1; padding-bottom: 10px; margin-bottom: 30px !important; 
    }
    
    /* Paneles Modulares Rectangulares de Precisión */
    .modular-panel {
        background-color: #FFFFFF;
        border: 1px solid #BDBDBD;
        padding: 20px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.15);
        color: #1A1A1A;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    
    /* Títulos fuera de los paneles (Labels) */
    .panel-label { color: #0D47A1; font-weight: bold; font-size: 0.9em; text-transform: uppercase; margin-bottom: 5px; }

    /* Alarma de Perforación Rectangular (Roja que respira) */
    @keyframes breathing {
      0% { border-color: #B71C1C; box-shadow: 0 0 5px #ff0000; }
      50% { border-color: #FF1744; box-shadow: 0 0 20px #ff0000; }
      100% { border-color: #B71C1C; box-shadow: 0 0 5px #ff0000; }
    }
    .alarm-active {
        animation: breathing 1.5s infinite ease-in-out;
        border: 3px solid #B71C1C;
        background-color: #FFCDD2;
        color: #B71C1C;
        padding: 15px;
        border-radius: 4px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1em;
        letter-spacing: 2px;
    }
    
    /* Métricas Técnicas Legibles */
    .stMetric label { color: #666 !important; font-weight: bold;}
    .stMetric .st-c3 { color: #0D47A1 !important; font-size: 2.2em !important; font-weight: bold; font-family: 'JetBrains Mono', monospace;}
    
    /* Sidebar Profesional */
    .sidebar .sidebar-content { background-color: #F5F5F5; }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL DE CALIBRACIÓN (SIDEBAR) ---
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

# --- CUERPO PRINCIPAL ---
st.markdown("<h1>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h1>", unsafe_allow_html=True)
st.caption(f"COORDENADAS DE PROSPECCIÓN CUÁNTICA | {time.strftime('%H:%M:%S')} UTC | ACCESO CONFIDENCIAL")

# Layout de 3 columnas (Simétrico)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    # PANEL 1: TARGET COORDINATES
    st.markdown('<div class="panel-label">📍 TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="modular-panel">
        <p><strong>LATITUDE:</strong> <span style="font-family: 'JetBrains Mono', monospace; color: #0D47A1;">{4.71 + (v1/1000):.4f}</span></p>
        <p><strong>LONGITUDE:</strong> <span style="font-family: 'JetBrains Mono', monospace; color: #0D47A1;">{-74.07 + (v2/1000):.4f}</span></p>
        <p><strong>REF-DEPTH:</strong> <span style="font-family: 'JetBrains Mono', monospace; color: #0D47A1; font-weight: bold; font-size: 1.2em;">{depth:.1f} m</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # PANEL 2: STREAM VARIATION
    st.markdown('<div class="panel-label">📊 STREAM VARIATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    flow_stability = np.random.randn(20) * (v4 / 15)
    st.line_chart(flow_stability, height=180)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # ESFERA AZUL CIELO CENTRAL (Tierra Dinámica)
    # Límite estricto para que el diamante NUNCA toque los bordes (Radio < 0.95)
    dx = np.clip(v1/500, -0.95, 0.95)
    dy = np.clip(v2/500, -0.95, 0.95)
    dz = np.clip(0.8 + (v6/400), -0.95, 0.95)

    fig = go.Figure()
    # Tierra Azul Cielo Traslúcida con Wireframe visible permanentemente
    phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.6, 
                             colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
                             contours=dict(x=dict(show=True, color="white", width=1),
                                           y=dict(show=True, color="white", width=1),
                                           z=dict(show=True, color="white", width=1))))
    
    # Objetivo Diamante Verde (Contenido en el volumen)
    fig.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                               marker=dict(size=18, color='#00FF00', symbol='diamond', line=dict(color='black', width=3))))

    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=650,
        modebar=dict(bgcolor='white', color='black')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

with col3:
    # PANEL 3: SYSTEM ANALYTICS (UNIFICADO)
    st.markdown('<div class="panel-label">🛡️ SYSTEM ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    
    st.metric("ÍNDICE DE SINCRO-COHERENCIA", f"{sync_score:.1f}%", delta=f"{v5:.1f} R-MASS")
    
    # Indicador de Perforación Rectangular
    if sync_score > 75:
        st.markdown('<div class="alarm-active">PUNTO DE PERFORACIÓN CONFIRMADO</div>', unsafe_allow_html=True)
    else:
        st.info("SCANNING SUBSURFACE...")
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PANEL 4: GEOPHYSICAL SIGNATURE (RADAR GRANDES DIMENSIONES)
    st.markdown('<div class="panel-label">⚡ GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel" style="padding: 10px;">', unsafe_allow_html=True)
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