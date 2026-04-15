import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN TÁCTICA: DISEÑO RESTAURADO CON FONDO GRIS OSCURO
st.set_page_config(page_title="SINCRO+ X | ABYSSAL NAVIGATOR", layout="wide")

# CSS: FONDO GRIS OSCURO Y TAMAÑOS MASIVOS
st.markdown("""
    <style>
    /* Fondo gris oscuro para resaltar ondas vivas */
    .stApp { background-color: #2D2D2D; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
    
    /* COHERENCIA INDEX GIGANTE */
    .coherence-value { font-size: 110px; font-weight: 900; color: #00E5FF; text-align: center; line-height: 1; margin: 0; }
    .coherence-label { font-size: 28px; color: #FFFFFF; text-align: center; text-transform: uppercase; letter-spacing: 5px; font-weight: bold; }
    
    /* ALERTA ROJA PARPADEANTE */
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .alarm-active { color: #FF0000 !important; animation: blink 0.5s infinite; text-shadow: 0 0 25px #FF0000; }
    
    /* CAJÓN DE TARGET ADQUISICIÓN (RESTRICTO A DISEÑO ANTERIOR) */
    .target-panel { background: rgba(255, 0, 0, 0.25); border: 3px solid #FF0000; padding: 25px; border-radius: 15px; text-align: center; }
    .coord-text { font-size: 45px; font-weight: bold; color: #FFFFFF; margin: 10px 0; }
    .target-title { color: #FF0000; font-size: 20px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# SUBSYSTEM INPUTS
with st.sidebar:
    st.header("📡 INPUT PARAMETERS")
    v_ten = st.slider("V-TENSOR (MAG)", -1.0, 1.0, 0.65)
    mag_f = st.slider("MAG-FLUX (GRAV)", -1.0, 1.0, 0.76)
    k_thr = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    c_mat = st.slider("C-MATRIX (VAL)", 1.0, 10.0, 9.2)
    r_mass = st.slider("R-MASS", 1.5, 4.5, 3.1)
    s_por = st.slider("STRAT-POR", 0.0, 40.0, 32.0)

# CÁLCULOS TÉCNICOS
raw_coherence = (c_mat * 7) + (s_por * 0.75) + (r_mass * 2)
coherence = min(100.0, raw_coherence)
depth = (k_thr / 4.5) + (r_mass * 118)

# LÓGICA DE ALERTA
is_gas = coherence > 88
status_color = "#FF0000" if is_gas else "#FFFF00" if coherence > 50 else "#00FF00"
blink_class = "alarm-active" if is_gas else ""

# --- CABECERA: COHERENCIA GIGANTE (RESTAURADA) ---
st.markdown('<p class="coherence-label">Coherence Index</p>', unsafe_allow_html=True)
st.markdown(f'<p class="coherence-value {blink_class}">{coherence:.1f}%</p>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:{status_color}; font-weight:bold; font-size:24px; margin-bottom:40px;">{ "GAS DETECTED - ABYSSAL SOURCE" if is_gas else "SCANNING..." }</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])

with col1:
    # 1. OSCILOSCOPIO CON ONDAS VIVAS (RESTABLECIDO)
    st.markdown("### 📊 WAVE OSCILLOSCOPE (DYNAMIC SYNC)")
    t = np.linspace(0, 10, 250)
    pulse = time.time() % 10
    
    fig_osc = go.Figure()
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*2.2 + pulse)*v_ten, name="V-TEN", line=dict(color='#FF3D00', width=3)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.cos(t*1.7 + pulse)*mag_f, name="MAG-F", line=dict(color='#00E676', width=3)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*3.0 + pulse)*0.6, name="C-MAT", line=dict(color='#D500F9', width=2)))
    
    fig_osc.update_layout(
        height=380, margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[-1.5, 1.5]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="white"))
    )
    st.plotly_chart(fig_osc, use_container_width=True)

    # 2. ARAÑA MASIVA (POSICIÓN ANTERIOR)
    st.markdown("### 🕸️ ISOTOPIC ARACHNID SIGNATURE")
    r_vals = [abs(v_ten)*100, abs(mag_f)*100, k_thr/9, c_mat*10, r_mass*22, s_por*2.5]
    theta = ['V-TEN', 'MAG-F', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=theta, fill='toself', 
        fillcolor='rgba(0, 229, 255, 0.4)', line=dict(color='#00E5FF', width=5)
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(255,255,255,0.05)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.2)", tickfont=dict(color="white")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.2)", tickfont=dict(size=16, color="#00E5FF"))
        ),
        showlegend=False, height=520, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=80,r=80,t=40,b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    # 3. TIERRA Y DIAMANTE (ALINEACIÓN EXACTA)
    st.markdown("### 🌍 DRILL POINT INTERSECTION")
    u, v = np.mgrid[0:2*np.pi:45j, 0:np.pi:45j]
    x, y, z = np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v)

    fig_earth = go.Figure(data=[go.Surface(x=x, y=y, z=z, opacity=0.85, colorscale='Viridis', showscale=False)])
    fig_earth.add_trace(go.Scatter3d(
        x=[v_ten], y=[mag_f], z=[np.sqrt(max(0, 1 - v_ten**2 - mag_f**2))],
        mode='markers', marker=dict(size=28, color='#FF0000', symbol='diamond', line=dict(color='white', width=3))
    ))

    fig_earth.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
        height=480, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_earth, use_container_width=True)

    # 4. CAJÓN TARGET ADQUISICIÓN (NÚMEROS GIGANTES Y TÍTULO RESTAURADO)
    st.markdown('<div class="target-panel">', unsafe_allow_html=True)
    st.markdown('<p class="target-title">TARGET ADQUISITION DATA</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text">LAT: {4.71 + (v_ten/100):.6f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text">LON: {-74.07 + (mag_f/100):.6f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text" style="color:#FF0000;">DEPTH: {depth:.1f} M</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# MOTOR DE VIBRACIÓN CONTINUA
time.sleep(0.1)
st.rerun()