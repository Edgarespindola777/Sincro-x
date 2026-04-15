import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# CONFIGURACIÓN DE PANTALLA
st.set_page_config(page_title="SINCRO+ X | MISSION CONTROL", layout="wide")

# LÓGICA DE CONTROL (SIDEBAR)
with st.sidebar:
    st.markdown("### 📡 SUBSYSTEM INPUT")
    v1 = st.slider("V-TENSOR (MAG)", -1.0, 1.0, 0.64) # Coordenada X
    v2 = st.slider("MAG-FLUX (GRAV)", -1.0, 1.0, 0.76) # Coordenada Y
    v3_thermal = st.slider("K-THERMAL", 300.0, 900.0, 450.0)
    v4_matrix = st.slider("C-MATRIX (VAL)", 1.0, 10.0, 7.5)
    v5_mass = st.slider("R-MASS", 1.5, 4.5, 2.8)
    v6_por = st.slider("STRAT-POR", 0.0, 40.0, 15.0)

# CÁLCULOS TÉCNICOS Y SINCRONÍA
sync_score = (v4_matrix * 8) + (v6_por / 2)
depth = (v3_thermal / 5) + (v5_mass * 100)

# LÓGICA DE POSICIÓN DEL DIAMANTE (INTERSECCIÓN EXACTA)
diamante_x, diamante_y = v1, v2
radius = 1.0
diamante_z = np.sqrt(max(0, radius**2 - diamante_x**2 - diamante_y**2)) + 0.05

# SEMÁFORO DE ESTADOS
if sync_score < 45:
    s_color, s_text, blink_class = "#2E7D32", "SCANNING: GREEN MODE", ""
elif sync_score < 85:
    s_color, s_text, blink_class = "#FBC02D", "SCANNING: ACQUISITION", ""
else:
    s_color, s_text, blink_class = "#B71C1C", "TARGET CONFIRMED", "blink-red"

# CSS: ESTÉTICA PROFESIONAL
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    @keyframes blink-red {{ 0% {{ background-color: #B71C1C; }} 50% {{ background-color: #ff4d4d; }} 100% {{ background-color: #B71C1C; }} }}
    .blink-red {{ animation: blink-red 0.5s infinite; color: white !important; }}
    .compact-status {{ background-color: white; border: 2px solid {s_color}; padding: 8px; border-radius: 8px; text-align: center; max-width: 250px; margin: auto; }}
    .panel-box {{ background-color: rgba(255,255,255,0.95); border: 2px solid #0D47A1; padding: 15px; border-radius: 5px; }}
    .data-value {{ font-size: 1.8em; font-weight: bold; color: #0D47A1; margin: 0; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #0D47A1;'>SINCRO+ X | PREDICTIVE GEODESY SYSTEM</h2>", unsafe_allow_html=True)

# --- PANEL SUPERIOR: COHERENCE INDEX COMPACTO ---
st.markdown(f"""
    <div class="compact-status">
        <p style="margin:0; font-size:0.7em; font-weight:bold;">COHERENCE INDEX: {sync_score:.1f}%</p>
        <div class="{blink_class}" style="background-color:{s_color}; color:white; padding:3px; border-radius:4px; font-weight:bold; font-size:0.8em;">
            {s_text}
        </div>
    </div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2.2, 1])

with col_left:
    # TARGET DATA CONDENSADO
    st.markdown('<p style="font-weight:bold; text-align:center; margin:0;">📍 TARGET ACQUISITION</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="panel-box">
            <p style="font-size:0.7em; margin:0;">X-VECTOR (LAT)</p>
            <p class="data-value">{4.71 + (v1/10):.5f}</p>
            <p style="font-size:0.7em; margin:10px 0 0 0;">Y-VECTOR (LON)</p>
            <p class="data-value">{-74.07 + (v2/10):.5f}</p>
            <p style="font-size:0.7em; margin:10px 0 0 0; color:#B71C1C;">DEPTH (M)</p>
            <p class="data-value" style="color:#B71C1C;">{depth:.1f}</p>
        </div>
    """, unsafe_allow_html=True)

    # OSCILOSCOPIO EN CAJA TÉCNICA (PLANO CARTESIANO)
    st.markdown('<p style="font-weight:bold; text-align:center; margin-top:15px;">📊 WAVE OSCILLOSCOPE</p>', unsafe_allow_html=True)
    t = np.linspace(0, 10, 100)
    noise = np.sin(t * v4_matrix) * np.exp(-t * 0.1) * v1
    fig_osc = go.Figure(data=go.Scatter(x=t, y=noise, line=dict(color='#0D47A1', width=2)))
    fig_osc.update_layout(
        height=200, margin=dict(l=20,r=20,b=20,t=10),
        xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True),
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True),
        paper_bgcolor='white', plot_bgcolor='white'
    )
    st.plotly_chart(fig_osc, use_container_width=True)

with col_center:
    # TIERRA GIGANTE Y SUBIDA
    steps = 40
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, opacity=0.85, colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
        contours=dict(x=dict(show=True, color="rgba(255,255,255,0.4)"), y=dict(show=True, color="rgba(255,255,255,0.4)"))
    )])
    
    # DIAMANTE INTERSECTANDO LAS VARIABLES
    fig_globe.add_trace(go.Scatter3d(
        x=[diamante_x], y=[diamante_y], z=[diamante_z],
        mode='markers', marker=dict(size=22, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond', line=dict(color='black', width=2))
    ))
    
    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, camera=dict(eye=dict(x=1.3, y=1.3, z=0.8))),
        margin=dict(l=0,r=0,b=0,t=0), height=750, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # ARAÑA GIGANTE CON VALORES NUMÉRICOS (SIN TÍTULO VACÍO)
    r_vals = [max(20, abs(v1)*50), max(20, abs(v2)*50), v3_thermal/9, v4_matrix*10, v5_mass*20, v6_por*2.2]
    categories = [f'V-TEN:{abs(v1):.1f}', f'MAG:{abs(v2):.1f}', f'K-THR:{v3_thermal:.0f}', 
                  f'C-MAT:{v4_matrix:.1f}', f'R-DEN:{v5_mass:.1f}', f'STRAT:{v6_por:.1f}']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=categories, fill='toself', fillcolor='rgba(13, 71, 161, 0.5)',
        line=dict(color='#0D47A1', width=4)
    ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 110]), angularaxis=dict(tickfont=dict(size=12, color="#0D47A1", font="Arial Black"))),
        showlegend=False, height=550, margin=dict(l=60, r=60, b=20, t=20), paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ALARMA SONORA
if sync_score >= 85:
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)