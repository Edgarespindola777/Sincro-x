import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X", layout="wide")

# LÓGICA DE CONTROL (SIDEBAR)
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# CÁLCULOS CRÍTICOS
sync_score = (v4 * 8) + (v6 / 2)
depth = (v3 / 5) + (v5 * 100)

# ESTADOS DEL SEMÁFORO
if sync_score < 45:
    s_color, s_text, blink_class = "#2E7D32", "SCANNING: INITIAL PHASE", "blink-active"
elif sync_score < 85:
    s_color, s_text, blink_class = "#FBC02D", "SCANNING: TARGET ACQUISITION", "blink-active"
else:
    s_color, s_text, blink_class = "#B71C1C", "DRILLING POINT CONFIRMED", "blink-fast"

# CSS: AJUSTES DE TAMAÑO Y PARPADEO
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.2; }} 100% {{ opacity: 1; }} }}
    .blink-active {{ animation: blink 1.5s infinite; }}
    .blink-fast {{ animation: blink 0.5s infinite; font-weight: bold; }}
    
    .central-box {{ 
        background-color: white; border: 2px solid {s_color}; padding: 10px; 
        border-radius: 8px; text-align: center; max-width: 400px; margin: auto;
    }}
    .panel-box {{ background-color: rgba(255,255,255,0.9); border: 2px solid #0D47A1; padding: 20px; border-radius: 5px; }}
    .coord-text {{ font-size: 2.2em; font-weight: bold; margin: 10px 0; }}
    .label-title {{ font-weight: bold; text-transform: uppercase; color: #0D47A1; text-align: center; font-size: 1em; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0D47A1; margin-bottom: 5px;'>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h2>", unsafe_allow_html=True)

# --- CABECERA: COHERENCE INDEX PEQUEÑO ---
st.markdown(f"""
    <div class="central-box">
        <p style="margin:0; font-weight:bold; font-size:0.8em;">COHERENCE INDEX</p>
        <h2 class="{blink_class}" style="margin:0; font-size: 2.5em;">{sync_score:.1f}%</h2>
        <div style="background-color:{s_color}; color:white; padding:5px; border-radius:4px; font-weight:bold; font-size: 0.9em;">
            {s_text}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
col_left, col_center, col_right = st.columns([1.2, 2, 1.2])

with col_left:
    st.markdown('<p class="label-title">📍 TARGET DATA</p>', unsafe_allow_html=True)
    # Parpadea solo cuando se encuentra el punto (sync_score >= 85)
    target_blink = "blink-fast" if sync_score >= 85 else ""
    st.markdown(f"""
        <div class="panel-box {target_blink}">
            <p style="margin:0; font-size:1em;">X-VECTOR (LAT)</p>
            <p class="coord-text">{4.71 + (v1/1000):.5f}</p>
            <hr>
            <p style="margin:0; font-size:1em;">Y-VECTOR (LON)</p>
            <p class="coord-text">{-74.07 + (v2/1000):.5f}</p>
            <hr>
            <p style="margin:0; font-size:1em; color:#B71C1C;">REF-DEPTH (M)</p>
            <p class="coord-text" style="color:#B71C1C;">{depth:.1f}</p>
        </div>
    """, unsafe_allow_html=True)

with col_center:
    # TIERRA AZUL CIELO - TAMAÑO INCREMENTADO
    # Corregido el error de 'pi' usando np.pi directamente
    steps = int(30 + (v6/2))
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, opacity=0.9, 
        colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], # Azul Cielo
        showscale=False,
        contours=dict(
            x=dict(show=True, color="white", width=1+(v4/4)), 
            y=dict(show=True, color="white", width=1+(v4/4))
        )
    )])
    
    fig_globe.add_trace(go.Scatter3d(
        x=[np.clip(v1/500, -0.9, 0.9)], y=[np.clip(v2/500, -0.9, 0.9)], z=[0.85],
        mode='markers', marker=dict(size=25, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond')
    ))
    
    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        margin=dict(l=0,r=0,b=0,t=0), height=700, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # GEOPHYSICAL SIGNATURE - ARAÑA GRANDE Y NEGRITA
    st.markdown('<p class="label-title">⚡ GEOPHYSICAL SIGNATURE</p>', unsafe_allow_html=True)
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    
    # Valores normalizados para asegurar visualización constante
    r_vals = [max(20, abs(v1)/5), max(20, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    categories = ['<b>V-TEN</b>', '<b>MAG</b>', '<b>K-THR</b>', '<b>C-MAT</b>', '<b>R-DEN</b>', '<b>STRAT</b>']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=categories, fill='toself', 
        fillcolor='rgba(13, 71, 161, 0.5)', line=dict(color='#0D47A1', width=4)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#BBB"),
            angularaxis=dict(tickfont=dict(size=14, color="#0D47A1", family="Arial Black"))
        ),
        showlegend=False, height=500, margin=dict(l=50, r=50, b=20, t=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUDIO DE HALLAZGO
if sync_score >= 85:
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)