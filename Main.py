import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# LÓGICA DE CONTROL (SIDEBAR)
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR (MAG)", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX (GRAV)", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX (VAL)", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# CÁLCULOS TÉCNICOS
sync_score = (v4 * 8) + (v6 / 2)
depth = (v3 / 5) + (v5 * 100)

# LÓGICA DE COLORES Y ALARMAS
if sync_score < 45:
    s_color, s_text, blink_class = "#2E7D32", "SCANNING: GREEN MODE", "" # Verde estático
elif sync_score < 85:
    s_color, s_text, blink_class = "#FBC02D", "SCANNING: ACQUISITION", "" # Amarillo
else:
    s_color, s_text, blink_class = "#B71C1C", "TARGET CONFIRMED", "blink-red" # Rojo parpadeante

# CSS AVANZADO
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    @keyframes blink-red {{ 0% {{ background-color: #B71C1C; }} 50% {{ background-color: #ff4d4d; }} 100% {{ background-color: #B71C1C; }} }}
    .blink-red {{ animation: blink-red 0.5s infinite; color: white !important; }}
    
    .status-box {{ 
        background-color: white; border: 2px solid {s_color}; padding: 10px; 
        border-radius: 8px; text-align: center; max-width: 350px; margin: auto;
    }}
    .compact-panel {{ 
        background-color: rgba(255,255,255,0.95); border: 2px solid #0D47A1; 
        padding: 15px; border-radius: 5px; text-align: center;
    }}
    .data-label {{ font-size: 0.8em; font-weight: bold; color: #555; margin: 0; }}
    .data-value {{ font-size: 1.8em; font-weight: bold; color: #0D47A1; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0D47A1; margin-bottom: 10px;'>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h2>", unsafe_allow_html=True)

# --- PANEL SUPERIOR: COHERENCE INDEX ESTÁTICO ---
st.markdown(f"""
    <div class="status-box">
        <p style="margin:0; font-weight:bold; font-size:0.8em;">COHERENCE INDEX</p>
        <h2 style="margin:0; font-size: 2.2em; color: #0D47A1;">{sync_score:.1f}%</h2>
        <div class="{blink_class}" style="background-color:{s_color}; color:white; padding:5px; border-radius:4px; font-weight:bold; transition: 0.5s;">
            {s_text}
        </div>
    </div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    # TARGET DATA CONDENSADO EN UN SOLO CAJÓN
    st.markdown('<p style="font-weight:bold; text-align:center;">📍 TARGET ACQUISITION</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="compact-panel">
            <p class="data-label">LATITUDE VECTOR</p>
            <p class="data-value">{4.71 + (v1/1000):.5f}</p>
            <p class="data-label">LONGITUDE VECTOR</p>
            <p class="data-value">{-74.07 + (v2/1000):.5f}</p>
            <p class="data-label" style="color:#B71C1C;">TARGET DEPTH</p>
            <p class="data-value" style="color:#B71C1C;">{depth:.1f} M</p>
        </div>
    """, unsafe_allow_html=True)

    # OSCILOSCOPIO (ONDA CIENTÍFICA)
    st.markdown('<p style="font-weight:bold; text-align:center; margin-top:20px;">🌊 STREAM OSCILLOSCOPE</p>', unsafe_allow_html=True)
    t = np.linspace(0, 4, 100)
    # La onda reacciona a los sliders
    y_wave = np.sin(t * v4) * np.cos(t * abs(v2/100))
    fig_wave = go.Figure(data=go.Scatter(x=t, y=y_wave, line=dict(color='#0D47A1', width=2)))
    fig_wave.update_layout(height=180, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', xaxis_visible=False, yaxis_visible=False)
    st.plotly_chart(fig_wave, use_container_width=True)

with col_center:
    # TIERRA DINÁMICA (MOVIMIENTO EN TIEMPO REAL)
    # La rotación (eye) cambia según v1 y v2
    steps = 30
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, opacity=0.8, 
        colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], # Azul Cielo
        showscale=False,
        contours=dict(
            x=dict(show=True, color="rgba(255,255,255,0.3)", width=1), # Líneas blancas suaves
            y=dict(show=True, color="rgba(255,255,255,0.3)", width=1)
        )
    )])
    
    # Marcador de diamante
    fig_globe.add_trace(go.Scatter3d(
        x=[np.clip(v1/500, -0.8, 0.8)], y=[np.clip(v2/500, -0.8, 0.8)], z=[0.85],
        mode='markers', marker=dict(size=20, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond')
    ))
    
    # El ángulo de visión cambia con los parámetros (Simulación de tiempo real)
    fig_globe.update_layout(
        scene=dict(
            xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
            camera=dict(eye=dict(x=1.5 + (v1/1000), y=1.5 + (v2/1000), z=1.0))
        ),
        margin=dict(l=0,r=0,b=0,t=0), height=650, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # GEOPHYSICAL SIGNATURE (ARAÑA)
    st.markdown('<p style="font-weight:bold; text-align:center;">⚡ GEOPHYSICAL SIGNATURE</p>', unsafe_allow_html=True)
    r_vals = [max(25, abs(v1)/5), max(25, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    categories = ['<b>V-TEN</b>', '<b>MAG</b>', '<b>K-THR</b>', '<b>C-MAT</b>', '<b>R-DEN</b>', '<b>STRAT</b>']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=categories, fill='toself', 
        fillcolor='rgba(13, 71, 161, 0.4)', line=dict(color='#0D47A1', width=3)
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 110], gridcolor="#BBB")),
        showlegend=False, height=450, margin=dict(l=40, r=40, b=20, t=20), paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# LÓGICA DE ALARMA SONORA Y TRANSICIÓN
if sync_score >= 85:
    # Alarma real al encontrar el punto
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)