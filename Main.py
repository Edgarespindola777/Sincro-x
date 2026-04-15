import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# CONFIGURACIÓN DE VISIBILIDAD MÁXIMA PARA CONGRESO
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# CSS: CONTRASTE ALTO SOBRE GRIS Y NÚMEROS MASIVOS
st.markdown("""
    <style>
    .stApp { background-color: #D1D5DB; color: #111827; font-family: 'Arial Black', sans-serif; }
    
    /* BLOQUE DE COHERENCIA Y TARGET */
    .header-panel { background: #FFFFFF; border: 4px solid #1E3A8A; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    .label-main { font-size: 35px; color: #1E3A8A; font-weight: bold; text-transform: uppercase; margin-bottom: 0px; }
    .huge-number { font-size: 140px; font-weight: 900; line-height: 1; margin: 10px 0; }
    
    /* ALERTA ROJA */
    @keyframes pulse-red { 0% { color: #991B1B; } 50% { color: #EF4444; } 100% { color: #991B1B; } }
    .alarm-text { animation: pulse-red 0.5s infinite; text-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    
    /* COORDENADAS GIGANTES */
    .coord-box { background: #FFFFFF; border-left: 15px solid #EF4444; padding: 20px; margin-top: 20px; border-radius: 10px; }
    .coord-val { font-size: 65px; font-weight: bold; color: #111827; margin: 0; }
    .coord-label { font-size: 25px; color: #EF4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# PARÁMETROS DE ENTRADA (SIDEBAR)
with st.sidebar:
    st.header("📡 SISTEMA DE ENTRADA")
    v_ten = st.slider("V-TENSOR (MAG)", -1.0, 1.0, 0.65)
    mag_f = st.slider("MAG-FLUX (GRAV)", -1.0, 1.0, 0.76)
    k_thr = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    c_mat = st.slider("C-MATRIX (VAL)", 1.0, 10.0, 9.2)
    r_mass = st.slider("R-MASS", 1.5, 4.5, 3.1)
    s_por = st.slider("STRAT-POR", 0.0, 40.0, 32.0)

# CÁLCULOS TÉCNICOS
raw_coherence = (c_mat * 7.5) + (s_por * 0.6) + (r_mass * 1.5)
coherence = min(100.0, raw_coherence)
depth = (k_thr / 4) + (r_mass * 120)
is_active = coherence > 85

# --- INTERFAZ SUPERIOR ---
st.markdown('<div class="header-panel">', unsafe_allow_html=True)
st.markdown('<p class="label-main">TARGET ACQUISITION | COHERENCE INDEX</p>', unsafe_allow_html=True)
color_num = "#EF4444" if is_active else "#1E3A8A"
blink_class = "alarm-text" if is_active else ""
st.markdown(f'<p class="huge-number {blink_class}" style="color:{color_num};">{coherence:.1f}%</p>', unsafe_allow_html=True)
if is_active:
    st.markdown('<p style="font-size:30px; color:#EF4444; font-weight:bold;">⚠️ GAS ABISAL DETECTADO - PUNTO DE IMPACTO ⚠️</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

col_viz, col_data = st.columns([1.8, 1.2])

with col_viz:
    # OSCILOSCOPIO MULTI-ONDA (VIBRACIÓN CONTINUA)
    st.markdown("### 📊 ANALIZADOR DE RUIDO Y SINCRONÍA")
    t = np.linspace(0, 10, 250)
    pulse = time.time() % 10
    
    fig_osc = go.Figure()
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*2.5 + pulse)*v_ten, name="V-TEN", line=dict(color='#1E3A8A', width=3)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.cos(t*1.8 + pulse)*mag_f, name="MAG-F", line=dict(color='#059669', width=3)))
    fig_osc.add_trace(go.Scatter(x=t, y=np.sin(t*3.2 + pulse)*0.6, name="C-MAT", line=dict(color='#DC2626', width=2)))
    
    fig_osc.update_layout(
        height=300, margin=dict(l=0,r=0,b=0,t=0),
        paper_bgcolor='rgba(255,255,255,0.8)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(gridcolor='rgba(0,0,0,0.1)', range=[-1.5, 1.5]),
        legend=dict(orientation="h", y=1.1, x=1)
    )
    st.plotly_chart(fig_osc, use_container_width=True)

    # ARAÑA MASIVA CENTRAL
    st.markdown("### 🕸️ FIRMA GEOFÍSICA INTEGRAL")
    r_vals = [abs(v_ten)*100, abs(mag_f)*100, k_thr/9, c_mat*10, r_mass*22, s_por*2.5]
    theta = ['V-TEN', 'MAG-F', 'K-THR', 'C-MAT', 'R-DEN', 'STRAT']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=theta, fill='toself', 
        fillcolor='rgba(30, 58, 138, 0.4)', line=dict(color='#1E3A8A', width=5)
    ))
    fig_radar.update_layout(
        polar=dict(bgcolor="white", radialaxis=dict(visible=True, range=[0, 100], gridcolor="#DDD"),
                   angularaxis=dict(gridcolor="#DDD", tickfont=dict(size=18, color="#1E3A8A"))),
        height=550, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=80,r=80,t=40,b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_data:
    # TIERRA COMPACTA E INTERSECCIÓN
    st.markdown("### 🌍 GEOLOCALIZACIÓN 3D")
    u, v = np.mgrid[0:2*np.pi:40j, 0:np.pi:40j]
    x, y, z = np.cos(u)*np.sin(v), np.sin(u)*np.sin(v), np.cos(v)
    
    fig_3d = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.9, showscale=False)])
    fig_3d.add_trace(go.Scatter3d(
        x=[v_ten], y=[mag_f], z=[np.sqrt(max(0, 1 - v_ten**2 - mag_f**2))],
        mode='markers', marker=dict(size=30, color='#EF4444', symbol='diamond', line=dict(color='white', width=3))
    ))
    fig_3d.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                        height=450, margin=dict(l=0,r=0,b=0,t=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_3d, use_container_width=True)

    # COORDENADAS GIGANTES (FONDO BLANCO SOBRE GRIS)
    st.markdown(f"""
        <div class="coord-box">
            <p class="coord-label">VECTOR LATITUD</p>
            <p class="coord-val">{4.71 + (v_ten/100):.6f}</p>
            <hr>
            <p class="coord-label">VECTOR LONGITUD</p>
            <p class="coord-val">{-74.07 + (mag_f/100):.6f}</p>
            <hr>
            <p class="coord-label">PROFUNDIDAD (M)</p>
            <p class="coord-val" style="color:#EF4444;">{depth:.1f}</p>
        </div>
    """, unsafe_allow_html=True)

# REFRESCO DE VIBRACIÓN
time.sleep(0.1)
st.rerun()