import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN TÁCTICA
st.set_page_config(page_title="SINCRO+ X | SINCRO-LOCALIZACIÓN", layout="wide")

# LÓGICA DE CONTROL (SIDEBAR)
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR (MAG)", -1.0, 1.0, 0.64) # Coordenada X
    v2 = st.slider("MAG-FLUX (GRAV)", -1.0, 1.0, 0.76) # Coordenada Y
    v3 = st.slider("R-MASS", 0.0, 1.0, 0.1) # Contribución Z

# CÁLCULOS DE POSICIÓN SINCRONIZADA
# Forzamos que la posición del diamante coincida EXACTAMENTE con los sliders
diamante_x = v1
diamante_y = v2
# Calculamos Z para que flote justo sobre la curvatura de la Tierra (Azul Cielo)
radius = 1.0
diamante_z = np.sqrt(max(0, radius**2 - diamante_x**2 - diamante_y**2)) + 0.1

# CSS PARA INTEGRACIÓN VISUAL
st.markdown("""
    <style>
    .stApp { background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }
    h1 { text-align: center; color: #0D47A1; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>SINCRO+ X | SISTEMA DE SINCRO-LOCALIZACIÓN</h1>", unsafe_allow_html=True)

# --- VISUALIZACIÓN 3D SINCRONIZADA ---
col_empty1, col_main, col_empty2 = st.columns([1, 3, 1])

with col_main:
    # TIERRA AZUL CIELO (SIN RECUADROS BLANCOS)
    steps = 35
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, opacity=0.9, 
        colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], # Azul Cielo
        showscale=False,
        contours=dict(
            x=dict(show=True, color="white", width=1), 
            y=dict(show=True, color="white", width=1)
        )
    )])
    
    # Marcador de Diamante (Verde por defecto, Rojo al encontrar el punto)
    fig_globe.add_trace(go.Scatter3d(
        x=[diamante_x], y=[diamante_y], z=[diamante_z],
        mode='markers+text',
        marker=dict(size=25, color='#00FF00', symbol='diamond', line=dict(color='black', width=2)),
        text=[f"ANOMALÍA DETECTADA<br>X: {diamante_x:.3f}<br>Y: {diamante_y:.3f}<br>Z: {diamante_z:.3f}"],
        textposition="top center",
        textfont=dict(color="black", size=14)
    ))
    
    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        margin=dict(l=0,r=0,b=0,t=0), height=750, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)