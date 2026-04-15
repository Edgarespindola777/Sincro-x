import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTA SEGURIDAD
st.set_page_config(page_title="SINCRO-X | DEEP CORE ANALYTICS", layout="wide")

# CSS: ESTÉTICA NASA / ORIÓN (Plata, Azul Abisal y Cromo)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@300;600&display=swap');
    .stApp { background: radial-gradient(circle, #0a192f 0%, #020c1b 100%); color: #e6f1ff; font-family: 'Share Tech Mono', monospace; }
    h1, h2 { font-family: 'Rajdhani', sans-serif; color: #64ffda; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0px 0px 10px #64ffda; }
    .stMetric { background: rgba(23, 42, 73, 0.7); border: 1px solid #64ffda; border-radius: 10px; padding: 15px; }
    .sidebar-text { font-size: 10px; color: #8892b0; }
    </style>
    """, unsafe_allow_html=True)

# BARRA LATERAL: CASCADA DE DATOS (HEX FLOW)
with st.sidebar:
    st.markdown("### DECRYPTING DATASTREAM")
    for _ in range(5):
        st.caption(f"0x{int(time.time()):x}..{np.random.randint(1000,9999)}..SYNC_OK")
    st.write("---")
    st.markdown("### SENSORES DE MATRIZ")
    v1 = st.slider("DTGQ (μGal)", -500.0, 500.0, -124.0)
    v2 = st.slider("VECTOR MAG. RESONANCE", 0.0, 100.0, 42.0)
    v3 = st.slider("EXCITACIÓN ENDÓGENA (K)", 273, 600, 450)
    v4 = st.number_input("CRISTAL RESONANCE INDEX", 2.0, 4.0, 2.85)
    v5 = st.selectbox("PROB-ALPHA PROTOCOL", ["ACTIVE", "STANDBY", "LOCKED"])

# CUERPO PRINCIPAL
st.title("🛰️ SINCRO-X : DEEP CORE ANALYTICS")
st.subheader("SISTEMA DE PROSPECCIÓN CUÁNTICA - PROYECTO JERICÓ")

col_left, col_mid, col_right = st.columns([1, 2, 1])

# COLUMNA IZQUIERDA: NÚMEROS EN MOVIMIENTO
with col_left:
    st.write("📡 TELEMETRÍA")
    placeholder = st.empty()
    # Simulación de flujo de datos
    df_data = pd.DataFrame(np.random.randn(10, 2), columns=['X-AXIS', 'Y-AXIS'])
    st.line_chart(df_data)
    st.markdown("<div style='color:#64ffda'>LATENCY: 0.002ms<br>BUFFER: 98%</div>", unsafe_allow_html=True)

# COLUMNA CENTRAL: LA TIERRA 3D (NASA STYLE)
with col_mid:
    # Generar esfera 3D
    phi = np.linspace(0, 2*np.pi, 50)
    theta = np.linspace(0, np.pi, 50)
    x = np.outer(np.cos(phi), np.sin(theta))
    y = np.outer(np.sin(phi), np.sin(theta))
    z = np.outer(np.ones(np.size(phi)), np.cos(theta))

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, 
                                     colorscale='Blues', 
                                     showscale=False, 
                                     opacity=0.3)])
    # Agregar punto del yacimiento
    fig.add_trace(go.Scatter3d(x=[0.2], y=[0.5], z=[0.8], 
                               mode='markers', 
                               marker=dict(size=10, color='#64ffda', symbol='diamond')))
    
    fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                      margin=dict(l=0, r=0, b=0, t=0), 
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      height=500)
    
    st.plotly_chart(fig, use_container_width=True)
    st.info("ANÁLISIS DE SINGULARIDAD EN CAPA DE BASAMENTO DETECTADO")

# COLUMNA DERECHA: ANALÍTICA AVANZADA
with col_right:
    st.write("📊 QUANTUM RESULTS")
    prob_real = (v3 / 6) + (v2 * 0.5)
    st.metric("ÍNDICE DE SINCRONÍA", f"{prob_real:.2f}%", delta="STABLE")
    
    # Gráfico de Radar para despistar
    categories = ['Tensión','Flujo','Masa','Calor','Resonancia']
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=[v1/10, v2, v3/6, v4*20, 50],
      theta=categories,
      fill='toself',
      line_color='#64ffda'
    ))
    fig_radar.update_layout(polar=dict(bgcolor='#0a192f'), showlegend=False, height=300, margin=dict(l=20, r=20, b=20, t=20))
    st.plotly_chart(fig_radar, use_container_width=True)

st.write("---")
st.caption(f"LOGOS PREDICTIVE ENGINE V.4.0 | AUTH: DR. ESPÍNDOLA NIÑO | {time.strftime('%Y-%m-%d %H:%M:%S')}")