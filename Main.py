import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import base64

# CONFIGURACIÓN TÁCTICA
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# LÓGICA DE CÁLCULO INICIAL PARA ESTADOS
if 'v1' not in st.session_state: v1, v2, v3, v4, v5, v6 = 120.0, -85.0, 450.0, 7.5, 2.8, 15.0
else: v1, v2, v3, v4, v5, v6 = st.session_state.v1, st.session_state.v2, st.session_state.v3, st.session_state.v4, st.session_state.v5, st.session_state.v6

# DETERMINACIÓN DE COLORES Y ESTADOS (SEMÁFORO)
sync_score = (v4 * 8) + (v6 / 2)
if sync_score < 45:
    status_color, status_text, blink_class = "#2E7D32", "COLD: SCANNING", "blink-slow" # Verde
elif sync_score < 85:
    status_color, status_text, blink_class = "#FBC02D", "WARMING: TARGET ACQUISITION", "blink-medium" # Amarillo
else:
    status_color, status_text, blink_class = "#B71C1C", "DRILLING POINT CONFIRMED", "blink-fast" # Rojo

# CSS: ANIMACIONES DE PARPADEO Y DISEÑO INTEGRADO
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    .main-title {{ color: #0D47A1; text-align: center; font-size: 2.2em; font-weight: bold; margin-bottom: 20px; }}
    
    /* ANIMACIONES DE PARPADEO */
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.1; }} 100% {{ opacity: 1; }} }}
    .blink-slow {{ animation: blink 2s infinite; }}
    .blink-medium {{ animation: blink 1s infinite; }}
    .blink-fast {{ animation: blink 0.5s infinite; font-weight: black; }}
    
    .value-box {{
        background-color: #FFFFFF; border: 3px solid {status_color}; padding: 15px;
        border-radius: 8px; font-size: 3em; font-weight: bold; text-align: center;
    }}
    .label-outside {{ color: #0D47A1; font-weight: bold; text-align: center; margin-bottom: 5px; }}
    
    .status-box {{
        background-color: {status_color}; color: white; padding: 15px;
        border-radius: 5px; text-align: center; font-size: 1.5em; margin-top: 10px;
    }}
    
    .coord-panel {{
        background-color: rgba(255, 255, 255, 0.9); border: 2px solid #0D47A1; padding: 20px;
        border-radius: 10px; text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# FUNCIÓN PARA EL SONIDO "BING BANG" (Simulado vía HTML5)
def play_discovery_sound():
    sound_html = f"""
        <audio autoplay loop>
        <source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg">
        </audio>
    """
    if sync_score >= 85:
        st.markdown(sound_html, unsafe_allow_html=True)

# SIDEBAR: CONTROLES
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

depth = (v3 / 5) + (v5 * 100)
st.markdown('<div class="main-title">SINCRO+ X | PREDICTIVE GEODESY SYSTEM</div>', unsafe_allow_html=True)

# --- CABECERA: COHERENCE INDEX Y CONFIRMACIÓN (PARPADEANTES) ---
c1, c2, c3 = st.columns([1, 1.5, 1])
with c2:
    st.markdown('<div class="label-outside">COHERENCE INDEX</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="value-box {blink_class}">{sync_score:.1f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="status-box {blink_class}">{status_text}</div>', unsafe_allow_html=True)
    play_discovery_sound()

# --- CUERPO: TIERRA FONDO Y COORDENADAS ---
col_l, col_r = st.columns([2.5, 1])

with col_l:
    # TIERRA AZUL CIELO INTEGRADA AL FONDO
    steps = int(25 + (v6/2))
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure()
    fig_globe.add_trace(go.Surface(
        x=x, y=y, z=z, opacity=0.85, colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
        contours=dict(x=dict(show=True, color="white", width=1+(v4/4)), y=dict(show=True, color="white", width=1+(v4/4)))
    ))
    
    dx, dy = np.clip(v1/500, -0.9, 0.9), np.clip(v2/500, -0.9, 0.9)
    fig_globe.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[0.85], mode='markers', 
                                   marker=dict(size=22, color='#FF0000' if sync_score > 85 else '#00FF00', 
                                               symbol='diamond', line=dict(color='black', width=3))))

    fig_globe.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                           paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=700)
    st.plotly_chart(fig_globe, use_container_width=True)

with col_r:
    # COORDENADAS RESALTADAS (PARPADEAN SI SE ENCUENTRA EL PUNTO)
    st.markdown('<div class="label-outside">DRILLING TARGET DATA</div>', unsafe_allow_html=True)
    blink_coord = blink_class if sync_score > 85 else ""
    
    st.markdown(f"""
        <div class="coord-panel {blink_coord}">
            <h3 style="color:#0D47A1; margin:0;">X-VECTOR (LAT)</h3>
            <p style="font-size: 1.8em; font-weight: bold;">{4.71 + (v1/1000):.5f}</p>
            <hr>
            <h3 style="color:#0D47A1; margin:0;">Y-VECTOR (LON)</h3>
            <p style="font-size: 1.8em; font-weight: bold;">{-74.07 + (v2/1000):.5f}</p>
            <hr>
            <h3 style="color:#B71C1C; margin:0;">REF-DEPTH</h3>
            <p style="font-size: 2.2em; font-weight: bold; color:#B71C1C;">{depth:.1f} M</p>
        </div>
    """, unsafe_allow_html=True)

    # GEOPHYSICAL SIGNATURE (ASEGURANDO VISIBILIDAD)
    st.markdown('<div class="label-outside" style="margin-top:20px;">GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    r_vals = [max(15, abs(v1)/5), max(15, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    fig_radar = go.Figure(data=go.Scatterpolar(r=r_vals, theta=['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT'], fill='toself', fillcolor='rgba(13, 71, 161, 0.4)', line=dict(color='#0D47A1', width=3)))
    fig_radar.update_layout(polar=dict(angularaxis=dict(tickfont=dict(size=12, color="#0D47A1", family="Arial Black"))), showlegend=False, height=350, margin=dict(l=40, r=40, b=20, t=20), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_radar, use_container_width=True)