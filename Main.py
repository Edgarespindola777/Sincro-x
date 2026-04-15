import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# LÓGICA DE CONTROL (SIDEBAR)
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

# DEFINICIÓN DE ESTADOS SEGÚN SYNC_SCORE
if sync_score < 45:
    s_color, s_text, blink = "#2E7D32", "SCANNING: INITIAL PHASE", "blink-slow"
elif sync_score < 85:
    s_color, s_text, blink = "#FBC02D", "SCANNING: TARGET ACQUISITION", "blink-medium"
else:
    s_color, s_text, blink = "#B71C1C", "DRILLING POINT CONFIRMED", "blink-fast"

# CSS PARA INTEGRACIÓN TOTAL
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.1; }} 100% {{ opacity: 1; }} }}
    .blink-fast {{ animation: blink 0.5s infinite; }}
    .central-box {{ background-color: white; border: 3px solid {s_color}; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px; }}
    .panel-box {{ background-color: rgba(255,255,255,0.8); border: 2px solid #0D47A1; padding: 15px; border-radius: 5px; }}
    .label-title {{ font-weight: bold; text-transform: uppercase; color: #0D47A1; margin-bottom: 8px; text-align: center; font-size: 0.9em; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0D47A1;'>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h2>", unsafe_allow_html=True)

# --- CABECERA: COHERENCE INDEX ---
c1, c2, c3 = st.columns([1, 1.5, 1])
with c2:
    st.markdown(f"""
        <div class="central-box">
            <p class="label-title">COHERENCE INDEX</p>
            <h1 class="{blink if sync_score > 85 else ''}" style="margin:0; font-size: 3.5em;">{sync_score:.1f}%</h1>
            <div style="background-color:{s_color}; color:white; padding:10px; margin-top:10px; border-radius:4px; font-weight:bold; font-size: 1.2em;">
                {s_text}
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- CUERPO DEL TABLERO ---
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    st.markdown('<p class="label-title">📍 TARGET DATA</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="panel-box {blink if sync_score > 85 else ''}">
            <p style="margin:5px;"><b>X-VECTOR:</b> {4.71 + (v1/1000):.5f}</p>
            <p style="margin:5px;"><b>Y-VECTOR:</b> {-74.07 + (v2/1000):.5f}</p>
            <h3 style="color:#B71C1C; margin:10px 0 0 0;">DEPTH: {depth:.1f} M</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="label-title" style="margin-top:20px;">📊 STREAM VARIATION</p>', unsafe_allow_html=True)
    st.line_chart(np.random.randn(20) * (v4/10), height=180)

with col_center:
    # TIERRA DINÁMICA SOBRE EL FONDO
    steps = int(25 + (v6/2))
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(x=x, y=y, z=z, opacity=0.8, colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False)])
    
    # Punto de perforación (Diamond)
    fig_globe.add_trace(go.Scatter3d(
        x=[np.clip(v1/500, -0.9, 0.9)], y=[np.clip(v2/500, -0.9, 0.9)], z=[0.85],
        mode='markers', marker=dict(size=20, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond', line=dict(color='black', width=2))
    ))
    
    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        margin=dict(l=0,r=0,b=0,t=0), height=550, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # --- GEOPHYSICAL SIGNATURE (ASEGURADA) ---
    st.markdown('<p class="label-title">⚡ GEOPHYSICAL SIGNATURE</p>', unsafe_allow_html=True)
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    
    # Normalización para que la araña nunca desaparezca
    r_vals = [max(20, abs(v1)/5), max(20, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=categories, fill='toself', 
        fillcolor='rgba(13, 71, 161, 0.4)', line=dict(color='#0D47A1', width=3)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#DDD"),
            angularaxis=dict(tickfont=dict(size=12, color="#0D47A1", family="Arial Black"))
        ),
        showlegend=False, height=400, margin=dict(l=30, r=30, b=20, t=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUDIO DISPARADO POR EL ÉXITO
if sync_score >= 85:
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)