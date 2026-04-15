import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE ALTA VISIBILIDAD PARA EL CONGRESO
st.set_page_config(page_title="SINCRO+ X | ABYSSAL NAVIGATOR", layout="wide")

# CSS: ANIMACIÓN Y DISEÑO DE IMPACTO
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* VALOR DE COHERENCIA GIGANTE */
    .coherence-value { font-size: 100px; font-weight: 900; color: #00E5FF; text-align: center; line-height: 1; margin: 0; }
    .coherence-label { font-size: 25px; color: #FFFFFF; text-align: center; text-transform: uppercase; letter-spacing: 5px; }
    
    /* ALERTA ROJA PARPADEANTE */
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .alarm-active { color: #FF0000 !important; animation: blink 0.4s infinite; text-shadow: 0 0 20px #FF0000; }
    
    /* CONTENEDOR DE DATOS COMPACTO */
    .target-panel { background: rgba(255, 0, 0, 0.2); border: 2px solid #FF0000; padding: 20px; border-radius: 15px; text-align: center; }
    .coord-text { font-size: 40px; font-weight: bold; color: #FFFFFF; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

# SUBSYSTEM INPUTS (Variables del Dr. Edgar)
with st.sidebar:
    st.header("📡 INPUT PARAMETERS")
    v_ten = st.slider("V-TENSOR (MAG)", -1.0, 1.0, 0.65)
    mag_f = st.slider("MAG-FLUX (GRAV)", -1.0, 1.0, 0.76)
    k_thr = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    c_mat = st.slider("C-MATRIX (VAL)", 1.0, 10.0, 9.2)
    r_mass = st.slider("R-MASS", 1.5, 4.5, 3.1)
    s_por = st.slider("STRAT-POR", 0.0, 40.0, 32.0)

# CÁLCULOS DE COHERENCIA Y SINCRONÍA
raw_coherence = (c_mat * 7) + (s_por * 0.7) + (r_mass * 2)
coherence = min(100.0, raw_coherence)
depth = (k_thr / 4.5) + (r_mass * 115)

# ESTADOS DE ALERTA
is_gas = coherence > 88
status_color = "#FF0000" if is_gas else "#FFFF00" if coherence > 50 else "#00FF00"
status_text = "GAS DETECTED - ABYSSAL SOURCE" if is_gas else "SCANNING..."
blink_class = "alarm-active" if is_gas else ""

# --- CABECERA: COHERENCIA GIGANTE ---
st.markdown(f'<p class="coherence-label">Coherence Index</p>', unsafe_allow_html=True)
st.markdown(f'<p class="coherence-value {blink_class}">{coherence:.1f}%</p>', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:{status_color}; font-weight:bold; font-size:20px; margin-bottom:30px;">{status_text}</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    # 1. OSCILOSCOPIO CON ONDAS QUE VIBRAN (MOTOR DINÁMICO)
    st.markdown("### 📊 WAVE OSCILLOSCOPE (DYNAMIC SYNC)")
    t = np.linspace(0, 10, 200)
    # Animación basada en tiempo real para que siempre "vibran"
    pulse = time.time() % 10
    
    fig_osc = go.Figure()
    # Cada variable tiene su propia onda constante
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*2 + pulse)*v_ten, name="V-TEN", line=dict(color='#FF0000', width=2)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.cos(t*1.5 + pulse)*mag_f, name="MAG-F", line=dict(color='#00E5FF', width=2)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*3 + pulse)*0.5, name="K-THR", line=dict(color='#FFFF00', width=1.5)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.cos(t*2.5 + pulse)*0.3, name="C-MAT", line=dict(color='#FF00FF', width=1.5)))
    
    fig_osc.update_layout(
        height=350, margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor='black', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[-1.5, 1.5]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_osc, use_container_width=True)

    # 2. ARAÑA MASIVA (CENTRALIZADA)
    st.markdown("### 🕸️ ISOTOPIC ARACHNID SIGNATURE")
    r_vals = [abs(v_ten)*100, abs(mag_f)*100, k_thr/9, c_mat*10, r_mass*22, s_por*2.5]
    theta = ['V-TENSOR', 'MAG-FLUX', 'K-THERMAL', 'C-MATRIX', 'R-MASS', 'STRAT-POR']
    
    fig_spider = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=theta, fill='toself', 
        fillcolor='rgba(0, 229, 255, 0.3)', line=dict(color='#00E5FF', width=4)
    ))
    fig_spider.update_layout(
        polar=dict(
            bgcolor="black",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#444"),
            angularaxis=dict(gridcolor="#444", tickfont=dict(size=14, color="#00E5FF"))
        ),
        showlegend=False, height=500, paper_bgcolor='black', margin=dict(l=80,r=80,t=20,b=20)
    )
    st.plotly_chart(fig_spider, use_container_width=True)

with col2:
    # 3. TIERRA Y DIAMANTE DE INTERSECCIÓN
    st.markdown("### 🌍 DRILL POINT INTERSECTION")
    steps = 50
    u, v = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x = np.cos(u)*np.sin(v)
    y = np.sin(u)*np.sin(v)
    z = np.cos(v)

    fig_earth = go.Figure(data=[go.Surface(x=x, y=y, z=z, opacity=0.8, colorscale='Ice', showscale=False)])
    
    # El diamante se ubica exactamente donde las variables se cruzan
    fig_earth.add_trace(go.Scatter3d(
        x=[v_ten], y=[mag_f], z=[np.sqrt(max(0, 1 - v_ten**2 - mag_f**2))],
        mode='markers', marker=dict(size=25, color='#FF0000', symbol='diamond', line=dict(color='white', width=2))
    ))

    fig_earth.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, aspectmode='data'),
        height=500, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='black'
    )
    st.plotly_chart(fig_earth, use_container_width=True)

    # 4. TARGET DATA PANEL (ROJO)
    st.markdown('<div class="target-panel">', unsafe_allow_html=True)
    st.markdown('<p style="color:#FF0000; font-weight:bold; margin:0;">TARGET ACQUISITION DATA</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text">LAT: {4.71 + (v_ten/100):.6f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text">LON: {-74.07 + (mag_f/100):.6f}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="coord-text" style="color:#FF0000;">DEPTH: {depth:.1f} M</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO-REFRESCAR PARA MANTENER LAS ONDAS VIBRANDO
time.sleep(0.1)
st.rerun()