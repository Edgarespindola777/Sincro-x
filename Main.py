import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X", layout="wide")

# LÓGICA DE VARIABLES INICIAL (Fuera del CSS para reactividad)
if 'v1' not in st.session_state:
    v1, v2, v3, v4, v5, v6 = 120.0, -85.0, 450.0, 7.5, 2.8, 15.0
else:
    v1, v2, v3, v4, v5, v6 = st.session_state.v1, st.session_state.v2, st.session_state.v3, st.session_state.v4, st.session_state.v5, st.session_state.v6

# CSS: ESTÉTICA DE FONDO INTEGRADO
st.markdown("""
    <style>
    .stApp { background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }
    .main-title { color: #0D47A1; text-align: center; font-size: 2em; font-weight: bold; margin-bottom: 20px; }
    
    .value-box {
        background-color: #FFFFFF; border: 2px solid #0D47A1; padding: 10px;
        border-radius: 5px; font-size: 2.5em; font-weight: bold; text-align: center;
    }
    .label-outside { color: #0D47A1; font-weight: bold; text-align: center; margin-bottom: 5px; text-transform: uppercase; }
    
    .status-indicator {
        font-size: 1.1em; font-weight: bold; padding: 8px; border-radius: 4px; text-align: center; margin-top: 10px;
    }
    
    .modular-panel {
        background-color: rgba(255, 255, 255, 0.8); border: 1px solid #BDBDBD; padding: 15px;
        border-radius: 4px; margin-bottom: 10px;
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

# CÁLCULOS DINÁMICOS
sync_score = (v4 * 8) + (v6 / 2)
depth = (v3 / 5) + (v5 * 100)

st.markdown('<div class="main-title">SINCRO+ X | PREDICTIVE GEODESY SYSTEM</div>', unsafe_allow_html=True)

# --- CABECERA DE COHERENCIA (NUEVA ESTRUCTURA) ---
c_col1, c_col2, c_col3 = st.columns([1, 1, 1])
with c_col2:
    st.markdown('<div class="label-outside">COHERENCE INDEX</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="value-box">{sync_score:.1f}%</div>', unsafe_allow_html=True)
    
    # Semáforo dinámico: Verde -> Amarillo -> Rojo
    if sync_score < 40:
        color, text = "#2E7D32", "SCANNING: INITIAL PHASE" # Verde
    elif sync_score < 85:
        color, text = "#FBC02D", "SCANNING: TARGET ACQUISITION" # Amarillo
    else:
        color, text = "#B71C1C", "DRILLING POINT CONFIRMED" # Rojo
        
    st.markdown(f'<div class="status-indicator" style="background-color:{color}; color:white;">{text}</div>', unsafe_allow_html=True)

# --- CUERPO PRINCIPAL ---
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    st.markdown('<div class="label-outside">TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="modular-panel">
        <p>LAT: {4.71 + (v1/1000):.4f} | LON: {-74.07 + (v2/1000):.4f}</p>
        <p style="font-size: 1.2em; font-weight: bold;">DEPTH: {depth:.1f} m</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="label-outside">STREAM VARIATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    st.line_chart(np.random.randn(20) * (v4/10), height=150)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    # TIERRA AZUL CIELO CON LÍNEAS DINÁMICAS
    # La rotación y densidad de malla dependen de v1 y v6
    steps = int(20 + (v6/2))
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure()
    fig_globe.add_trace(go.Surface(
        x=x, y=y, z=z, 
        opacity=0.8, 
        colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], # Azul Cielo
        showscale=False,
        contours=dict(
            x=dict(show=True, color="white", width=1 + (v4/5)),
            y=dict(show=True, color="white", width=1 + (v4/5))
        )
    ))
    
    # Diamante de localización
    dx, dy = np.clip(v1/500, -0.9, 0.9), np.clip(v2/500, -0.9, 0.9)
    fig_globe.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[0.8], mode='markers', 
                                   marker=dict(size=15, color='#00FF00', symbol='diamond')))

    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0,r=0,b=0,t=0), height=600
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # GEOPHYSICAL SIGNATURE (FORZADA PARA VISIBILIDAD)
    st.markdown('<div class="label-outside">GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown('<div class="modular-panel">', unsafe_allow_html=True)
    
    categories = ['V-TEN', 'MAG', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    # Normalización para asegurar que la araña nunca sea 0
    r_values = [max(10, abs(v1)/5), max(10, abs(v2)/5), v3/9, v4*10, v5*20, v6*2.2]
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_values, theta=categories, fill='toself', 
        fillcolor='rgba(13, 71, 161, 0.4)', line=dict(color='#0D47A1', width=3)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 110], gridcolor="#DDD"),
            angularaxis=dict(tickfont=dict(size=12, color="#0D47A1", family="Arial Black"))
        ),
        showlegend=False, height=400, margin=dict(l=40, r=40, b=20, t=20),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)