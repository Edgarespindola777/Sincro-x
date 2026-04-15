import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE ALTA PRECISIÓN
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# CSS: ENFOQUE EN EL CENTRO DE MANDO
st.markdown("""
    <style>
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Courier New', monospace; }
    h1 { color: #0D47A1; text-align: center; font-size: 2.2em !important; margin-bottom: 10px; border-bottom: 2px solid #0D47A1; }
    
    /* Panel de Confirmación Centralizado (Arriba de la Tierra) */
    .central-command {
        background-color: #FFFFFF; border: 2px solid #0D47A1; padding: 15px;
        border-radius: 8px; box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
        text-align: center; margin-bottom: 20px;
    }
    
    .modular-panel {
        background-color: #FFFFFF; border: 1px solid #BDBDBD; padding: 15px;
        border-radius: 4px; box-shadow: 4px 4px 10px rgba(0,0,0,0.1); margin-bottom: 15px;
    }
    
    .panel-label { color: #0D47A1; font-weight: bold; text-transform: uppercase; font-size: 0.9em; margin-bottom: 5px; }

    .alarm-confirmed {
        background-color: #B71C1C; color: white; padding: 12px;
        border-radius: 4px; font-weight: bold; font-size: 1.3em;
        letter-spacing: 2px; animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR: ENTRADA DE DATOS
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# LÓGICA DE CÁLCULO
sync_score = (v4 * 8) + (v6 / 2)
depth = (v3 / 5) + (v5 * 100)

st.markdown("<h1>SINCRO+ X | ANALÍTICA GEODÉSICA</h1>", unsafe_allow_html=True)

# --- FILA SUPERIOR: COMANDO CENTRAL (LO QUE USTED PIDIÓ) ---
col_empty1, col_main, col_empty2 = st.columns([1, 2, 1])
with col_main:
    st.markdown('<div class="central-command">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.metric("COHERENCE INDEX", f"{sync_score:.1f}%", delta=f"{v4} CM")
    with c2:
        if sync_score > 75:
            st.markdown('<div class="alarm-confirmed">PUNTO CONFIRMADO</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#666; font-weight:bold; padding-top:15px;">ANALYZING SUBSURFACE...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- FILA INFERIOR: VISUALIZACIÓN Y TELEMETRÍA ---
col_left, col_center, col_right = st.columns([1, 1.8, 1])

with col_left:
    st.markdown('<div class="panel-label">📍 TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="modular-panel">
        <p>LAT: {4.71 + (v1/1000):.4f}</p>
        <p>LON: {-74.07 + (v2/1000):.4f}</p>
        <p style="font-size: 1.4em; font-weight: bold; color: #0D47A1;">{depth:.1f} m</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="panel-label">📊 STREAM VARIATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    st.line_chart(np.random.randn(20) * (v4/10), height=150)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    # TIERRA CENTRAL
    fig_globe = go.Figure()
    phi, theta = np.mgrid[0:2*np.pi:35j, 0:np.pi:35j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    fig_globe.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.7, colorscale='Ice', showscale=False))
    
    # Diamante Confinado
    dx, dy = np.clip(v1/600, -0.9, 0.9), np.clip(v2/600, -0.9, 0.9)
    fig_globe.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[0.85], mode='markers', 
                                   marker=dict(size=18, color='#00FF00', symbol='diamond', line=dict(color='black', width=2))))
    
    fig_globe.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), 
                           margin=dict(l=0,r=0,b=0,t=0), height=550)
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    st.markdown('<div class="panel-label">⚡ GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel" style="padding: 5px;">', unsafe_allow_html=True)
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    r_values = [abs(v1)/5, abs(v2)/5, v3/9, v4*10, v5*20, v6*2]
    
    fig_radar = go.Figure(data=go.Scatterpolar(r=r_values, theta=categories, fill='toself', fillcolor='rgba(135, 206, 235, 0.6)', line=dict(color='#0D47A1', width=3)))
    fig_radar.update_layout(
        polar=dict(angularaxis=dict(tickfont=dict(size=14, color="#0D47A1", family="Arial Black"))),
        showlegend=False, height=380, margin=dict(l=40,r=40,b=20,t=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)