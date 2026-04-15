import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN MISSION CONTROL
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# CSS: ESTÉTICA DE INSTRUMENTACIÓN EQUILIBRADA
st.markdown("""
    <style>
    .stApp { background-color: #E0E0E0; color: #1A1A1A; font-family: 'Courier New', monospace; }
    
    /* Título Superior Discreto */
    .main-title { 
        color: #0D47A1; text-align: center; font-size: 22px; 
        font-weight: bold; border-bottom: 1px solid #0D47A1; margin-bottom: 30px;
    }

    /* Títulos fuera de los círculos */
    .label-title { color: #0D47A1; font-weight: bold; font-size: 14px; margin-bottom: 5px; text-align: center; }

    /* Círculos de Información */
    .circle-panel {
        background-color: #FFFFFF;
        border: 1px solid #BDBDBD;
        border-radius: 50%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        margin: auto; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }

    /* Indicador de Confirmación (Pequeño) */
    .status-indicator {
        width: 120px; height: 120px; border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-size: 10px; text-align: center; font-weight: bold; margin: auto;
    }
    .status-confirmed { background-color: #FFCDD2; border: 2px solid #F44336; color: #B71C1C; animation: pulse 2s infinite; }
    .status-scanning { background-color: #FFF9C4; border: 2px solid #FBC02D; color: #F57F17; }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR CALIBRATION
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR", -500.0, 500.0, 120.0)
    v2 = st.slider("MAG-FLUX", -500.0, 500.0, -85.0)
    v3 = st.slider("K-THERMAL", 300, 900, 450)
    v4 = st.slider("C-MATRIX", 1.0, 10.0, 7.5)
    v5 = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6 = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# LOGICA
depth = (v3 / 5) + (v5 * 100)
sync_score = (v4 * 8) + (v6 / 2)

st.markdown('<div class="main-title">SINCRO+ X | PREDICTIVE GEODESY SYSTEM</div>', unsafe_allow_html=True)

# LAYOUT DE 3 COLUMNAS
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_left:
    st.markdown('<div class="label-title">TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="circle-panel" style="width: 240px; height: 240px;">
        <span style="font-size: 12px; color: #666;">LAT: {4.71 + (v1/1000):.4f}</span>
        <span style="font-size: 12px; color: #666;">LON: {-74.07 + (v2/1000):.4f}</span>
        <span style="font-size: 20px; font-weight: bold; color: #0D47A1; margin-top:10px;">{depth:.1f} m</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 40px;" class="label-title">STREAM VARIATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="circle-panel" style="width: 240px; height: 240px; padding: 20px;">', unsafe_allow_html=True)
    st.line_chart(np.random.randn(15), height=140, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_center:
    # TIERRA GRANDE Y DIAMANTE CONFINADO
    # Limitamos dx y dy para que el diamante nunca toque los bordes (Radio < 0.85)
    dx = np.clip(v1/600, -0.85, 0.85)
    dy = np.clip(v2/600, -0.85, 0.85)
    dz = np.clip(0.7 + (v6/500), -0.85, 0.85)

    fig = go.Figure()
    phi, theta = np.mgrid[0:2*np.pi:40j, 0:np.pi:40j]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig.add_trace(go.Surface(x=x, y=y, z=z, opacity=0.7, 
                             colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
                             contours=dict(x=dict(show=True, color="white", width=1),
                                           y=dict(show=True, color="white", width=1),
                                           z=dict(show=True, color="white", width=1))))
    
    fig.add_trace(go.Scatter3d(x=[dx], y=[dy], z=[dz], mode='markers',
                               marker=dict(size=20, color='#00FF00', symbol='diamond', line=dict(color='black', width=2))))

    fig.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,b=0,t=0), height=600
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<div class="label-title">SYSTEM ANALYTICS</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="circle-panel" style="width: 240px; height: 240px;">
        <span style="font-size: 11px; color: #666;">COHERENCE INDEX</span>
        <span style="font-size: 32px; font-weight: bold; color: #0D47A1;">{sync_score:.1f}%</span>
        <div style="margin-top: 15px;" class="status-indicator {'status-confirmed' if sync_score > 75 else 'status-scanning'}">
            {'POINT<br>CONFIRMED' if sync_score > 75 else 'SCANNING<br>CORE...'}
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="margin-top: 40px;" class="label-title">GEOPHYSICAL SIGNATURE</div>', unsafe_allow_html=True)
    st.markdown('<div class="circle-panel" style="width: 240px; height: 240px; padding: 10px;">', unsafe_allow_html=True)
    categories = ['V-T', 'MAG', 'K-T', 'C-M', 'R-M', 'STR']
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=[abs(v1/5), abs(v2/5), v3/9, v4*10, v5*20, v6*2], theta=categories, fill='toself', 
        fillcolor='rgba(0, 191, 255, 0.4)', line=dict(color='#0D47A1', width=2)
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="white", radialaxis=dict(visible=False)),
        showlegend=False, margin=dict(l=30,r=30,t=30,b=30), height=200
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)