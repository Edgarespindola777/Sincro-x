import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE ALTA PRECISIÓN - SIN ERRORES
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# CSS: ESTÉTICA MODULAR CIENTÍFICA (HIGH-LEGIBILITY)
st.markdown("""
    <style>
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Courier New', monospace; }
    h1 { color: #0D47A1; text-align: center; border-bottom: 2px solid #0D47A1; padding-bottom: 10px; margin-bottom: 20px; }
    
    .modular-panel {
        background-color: #FFFFFF; border: 1px solid #BDBDBD; padding: 20px;
        border-radius: 4px; box-shadow: 4px 4px 12px rgba(0,0,0,0.15); margin-bottom: 15px;
    }
    
    .panel-label { 
        color: #0D47A1; font-weight: bold; text-transform: uppercase; 
        font-size: 1.1em; margin-bottom: 5px;
    }

    .alarm-active {
        border: 3px solid #B71C1C; background-color: #FFCDD2; color: #B71C1C;
        padding: 15px; border-radius: 4px; text-align: center; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR: CONTROL DE SUBSISTEMAS
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM CALIBRATION")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# LÓGICA DE DATOS
depth = (v3 / 5) + (v5 * 100)
sync_score = (v4 * 8) + (v6 / 2)

st.markdown("<h1>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h1>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 1.8, 1.2])

with col_left:
    st.markdown('<div class="panel-label">📍 TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="modular-panel">
        <p>LAT: <span style="color:#0D47A1;">{4.71 + (v1/1000):.4f}</span></p>
        <p>LON: <span style="color:#0D47A1;">{-74.07 + (v2/1000):.4f}</span></p>
        <p style="font-size: 1.3em; font-weight: bold; color: #0D47A1;">{depth:.1f} m</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="panel-label">📊 STREAM VARIATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    st.line_chart(np.random.randn(20) * (v4/10), height=200)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    # TIERRA Y DIAMANTE (ERROR CORREGIDO: np.pi)
    dx, dy = np.clip(v1/550, -0.9, 0.9), np.clip(v2/550, -0.9, 0.9)
    dz = np.clip(0.75 + (v6/450), -0.9, 0.9)

    fig_globe = go.Figure()
    # Aquí es donde estaba el error: se agregó np.pi
    phi, theta = np.mgrid[0:2*np.pi:35j, 0:np.pi:35j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.6, colorscale='Ice', showscale=False,
                                  contours=dict(x=dict(show=True, color="white"), y=dict(show=True, color="white"))))
    
    fig_globe.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                                   marker=dict(size=18, color='#00FF00', symbol='diamond', line=dict(color='black', width=3))))

    fig_globe.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                           paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=650)
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # --- GEOPHYSICAL SIGNATURE: MÁS ARRIBA, MÁS GRANDE, LETRAS RESALTADAS ---
    st.markdown('<div class="panel-label">⚡ GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel" style="padding: 10px;">', unsafe_allow_html=True)
    
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    r_values = [abs(v1)/4.5, abs(v2)/4.5, v3/8, v4*11, v5*22, v6*2.2]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_values, theta=categories, fill='toself', 
        fillcolor='rgba(135, 206, 235, 0.6)', line=dict(color='#0D47A1', width=3)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#DDD"),
            angularaxis=dict(
                tickfont=dict(size=15, color="#0D47A1", family="Arial Black"), # Letras más grandes y negrita
                rotation=90, direction="clockwise"
            ),
            bgcolor="white"
        ),
        showlegend=False, height=450, margin=dict(l=45, r=45, b=30, t=30)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel-label">🛡️ ANALYTICS STATUS</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    st.metric("COHERENCE INDEX", f"{sync_score:.1f}%")
    if sync_score > 75:
        st.markdown('<div class="alarm-active">PUNTO CONFIRMADO</div>', unsafe_allow_html=True)
    else:
        st.info("SCANNING DATA...")
    st.markdown('</div>', unsafe_allow_html=True)