import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X", layout="wide")

# LÓGICA DE ESTADO
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

sync_score = (v4 * 8) + (v6 / 2)
depth = (v3 / 5) + (v5 * 100)

if sync_score < 45:
    s_color, s_text, blink = "#2E7D32", "COLD: SCANNING", "blink-slow"
elif sync_score < 85:
    s_color, s_text, blink = "#FBC02D", "WARMING: TARGET ACQUISITION", "blink-medium"
else:
    s_color, s_text, blink = "#B71C1C", "DRILLING POINT CONFIRMED", "blink-fast"

# ESTILOS PARA RESTAURAR TODOS LOS CUADROS
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.1; }} 100% {{ opacity: 1; }} }}
    .blink-fast {{ animation: blink 0.5s infinite; }}
    .central-box {{ background-color: white; border: 3px solid {s_color}; padding: 15px; border-radius: 8px; text-align: center; }}
    .coord-panel {{ background-color: white; border: 2px solid #0D47A1; padding: 15px; border-radius: 5px; text-align: center; }}
    .label-title {{ font-weight: bold; text-transform: uppercase; margin-bottom: 5px; font-size: 0.9em; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h2>", unsafe_allow_html=True)

# --- CABECERA DE IMPACTO ---
c1, c2, c3 = st.columns([1, 1.5, 1])
with c2:
    st.markdown(f"""
        <div class="central-box">
            <p class="label-title">COHERENCE INDEX</p>
            <h1 class="{blink if sync_score > 85 else ''}" style="margin:0;">{sync_score:.1f}%</h1>
            <div style="background-color:{s_color}; color:white; padding:10px; margin-top:10px; border-radius:4px; font-weight:bold;">
                {s_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- FILA DE DATOS Y VISUALIZACIÓN ---
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    st.markdown('<p class="label-title">📍 TARGET DATA</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="coord-panel {blink if sync_score > 85 else ''}">
            <p>LAT: {4.71 + (v1/1000):.5f}</p>
            <p>LON: {-74.07 + (v2/1000):.5f}</p>
            <h3 style="color:#B71C1C;">DEPTH: {depth:.1f} M</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="label-title" style="margin-top:20px;">📊 STREAM VARIATION</p>', unsafe_allow_html=True)
    st.line_chart(np.random.randn(20) * (v4/10), height=150)

with col_center:
    # TIERRA DINÁMICA
    steps = int(25 + (v6/2))
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, opacity=0.8, colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False)])
    fig.add_trace(go.Scatter3d(x=[np.clip(v1/500, -0.9, 0.9)], y=[np.clip(v2/500, -0.9, 0.9)], z=[0.85], mode='markers', marker=dict(size=18, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond')))
    fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False), margin=dict(l=0,r=0,b=0,t=0), height=500, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<p class="label-title">⚡ GEOPHYSICAL SIGNATURE</p>', unsafe_allow_html=True)
    r_vals = [max(15, abs(v1)/5), max(15, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    fig_radar = go.Figure(data=go.Scatterpolar(r=r_vals, theta=['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT'], fill='toself', fillcolor='rgba(13, 71, 161, 0.4)', line=dict(color='#0D47A1', width=3)))
    fig_radar.update_layout(polar=dict(angularaxis=dict(tickfont=dict(size=10))), showlegend=False, height=350, margin=dict(l=40, r=40, b=20, t=20), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_radar, use_container_width=True)

if sync_score >= 85:
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)