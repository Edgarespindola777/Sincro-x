import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# CONFIGURACIÓN TÁCTICA Y ESTÉTICA IMPECABLE
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

# SEMÁFORO DE ESTADOS Y ALERTAS
if sync_score < 45:
    s_color, s_text, blink_class = "#2E7D32", "SCANNING: INITIAL PHASE", "" # Verde
elif sync_score < 85:
    s_color, s_text, blink_class = "#FBC02D", "SCANNING: ACQUISITION", "" # Amarillo
else:
    s_color, s_text, blink_class = "#B71C1C", "DRILLING POINT CONFIRMED", "blink-red" # Rojo parpadeante

# CSS AVANZADO: ESTÉTICA DE ALTA INGENIERÍA
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E0E0E0; color: #0D47A1; font-family: 'Courier New', monospace; }}
    
    @keyframes blink-red {{ 0% {{ background-color: #B71C1C; }} 50% {{ background-color: #ff4d4d; }} 100% {{ background-color: #B71C1C; }} }}
    .blink-red {{ animation: blink-red 0.5s infinite; color: white !important; font-weight: bold; font-size: 1.1em; }}
    
    .status-compact {{ 
        background-color: white; border: 2px solid {s_color}; padding: 8px; border-radius: 6px; 
        text-align: center; max-width: 250px; margin: auto; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }}
    .huge-red-panel {{ 
        background-color: rgba(183, 28, 28, 0.95); border: 2px solid #fff; padding: 15px; border-radius: 10px; text-align: center;
        width: 300px; margin: auto; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }}
    .data-value {{ font-size: 1.7em; font-weight: bold; color: #fff; margin: 0; }}
    .panel-box {{ background-color: rgba(255,255,255,0.9); border: 1px solid #0D47A1; padding: 15px; border-radius: 5px; }}
    .label-title {{ font-weight: bold; text-transform: uppercase; color: #0D47A1; text-align: center; font-size: 0.9em; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #0D47A1;'>SINCRO+ X | ABYSSAL GAS NAVIGATOR</h1>", unsafe_allow_html=True)

# --- PANEL SUPERIOR: COHERENCE INDEX COMPACTO ---
st.markdown(f"""
    <div class="status-compact">
        <p style="margin:0; font-size:0.7em; font-weight:bold;">COHERENCE: {sync_score:.1f}%</p>
        <div class="{blink_class}" style="background-color:{s_color}; color:white; padding:4px; border-radius:3px; font-weight:bold; font-size:0.8em;">
            {s_text}
        </div>
    </div>
""", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1.2, 2.3, 1.2])

with col_left:
    # OSCILOSCOPIO MULTIVARIABLE (TODAS LAS ONDAS)
    st.markdown('<p class="label-title">📊 WAVE OSCILLOSCOPE</p>', unsafe_allow_html=True)
    t = np.linspace(0, 10, 100)
    wave_cmat = np.sin(t * (1.5 + v4_matrix/2)) * 0.7 # Azul (C-MAT)
    wave_strat = np.cos(t * (2.0 + v6_por/10)) * 0.4 # Verde (STRAT)
    wave_mag = np.sin(t * (2.5 + abs(v1))) * np.exp(-t * 0.02) # Rojo (MAG)
    wave_grav = np.cos(t * (3.0 + abs(v2))) * np.exp(-t * 0.03) # Amarillo (GRAV)
    wave_mass = np.sin(t * (3.5 + v5_mass)) * 0.2 # Morado (R-DEN)

    fig_osc = go.Figure()
    fig_osc.add_trace(go.Scatter(x=t, y=wave_cmat, name="C-MAT", line=dict(color='#0D47A1', width=1.5)))
    fig_osc.add_trace(go.Scatter(x=t, y=wave_strat, name="STRAT", line=dict(color='#2E7D32', width=1.5)))
    fig_osc.add_trace(go.Scatter(x=t, y=wave_mag, name="MAG", line=dict(color='#B71C1C', width=1.5)))
    fig_osc.add_trace(go.Scatter(x=t, y=wave_grav, name="GRAV", line=dict(color='#FBC02D', width=1.5)))
    fig_osc.add_trace(go.Scatter(x=t, y=wave_mass, name="R-DEN", line=dict(color='#6A1B9A', width=1.5)))

    fig_osc.update_layout(
        height=220, margin=dict(l=10,r=10,b=20,t=10),
        xaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True),
        yaxis=dict(showgrid=True, gridcolor='lightgray', zeroline=True),
        paper_bgcolor='white', plot_bgcolor='white', showlegend=True, legend=dict(font=dict(size=8))
    )
    st.plotly_chart(fig_osc, use_container_width=True)

with col_center:
    # TIERRA GIGANTE CON LÍNEAS DINÁMICAS Y SUAVES
    steps = 45
    phi, theta = np.mgrid[0:2*np.pi:complex(steps), 0:np.pi:complex(steps)]
    x, y, z = np.cos(phi)*np.sin(theta), np.sin(phi)*np.sin(theta), np.cos(theta)
    
    fig_globe = go.Figure(data=[go.Surface(
        x=x, y=y, z=z, opacity=0.85, colorscale=[[0, '#87CEEB'], [1, '#00BFFF']], showscale=False,
        contours=dict(
            x=dict(show=True, color="rgba(255,255,255,0.35)", width=1), 
            y=dict(show=True, color="rgba(255,255,255,0.35)", width=1)
        )
    )])
    
    # DIAMANTE INTERSECTANDO EXACTAMENTE
    fig_globe.add_trace(go.Scatter3d(
        x=[diamante_x], y=[diamante_y], z=[diamante_z],
        mode='markers', marker=dict(size=22, color='#FF0000' if sync_score > 85 else '#00FF00', symbol='diamond', line=dict(color='black', width=1.5))
    ))
    
    # El ángulo de visión cambia con los parámetros (Simulación de tiempo real)
    fig_globe.update_layout(
        scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False,
                   camera=dict(eye=dict(x=1.3, y=1.3, z=0.7))),
        margin=dict(l=0,r=0,b=0,t=0), height=750, paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_globe, use_container_width=True)

with col_right:
    # CAJA DE TARGET DATA (MASIVA Y ROJA COMPACTA)
    st.markdown('<p class="label-title">📍 TARGET ACQUISITION</p>', unsafe_allow_html=True)
    coord_blink = "blink-red" if sync_score > 85 else ""
    coord_size = "2.3em" if sync_score > 85 else "1.7em" # Se agrandan al encontrar el punto
    st.markdown(f"""
        <div class="huge-red-panel {coord_blink}">
            <p style="font-size:0.7em; margin:0; color:#fff;">X-VECTOR (LAT)</p>
            <p class="data-value" style="font-size:{coord_size};">{4.71 + (v1/10):.5f}</p>
            <p style="font-size:0.7em; margin:10px 0 0 0; color:#fff;">Y-VECTOR (LON)</p>
            <p class="data-value" style="font-size:{coord_size};">{-74.07 + (v2/10):.5f}</p>
            <p style="font-size:0.7em; margin:10px 0 0 0; color:#fff;">REF-DEPTH</p>
            <p class="data-value" style="color:#FBC02D; font-size:{coord_size};">{depth:.1f} M</p>
        </div>
    """, unsafe_allow_html=True)

    # ARAÑA MASIVA CON VALORES NUMÉRICOS (TITULO ELIMINADO)
    st.markdown('<p class="label-title" style="margin-top:20px;">⚡ ISOTOPIC VARIATION</p>', unsafe_allow_html=True)
    r_vals = [max(15, abs(v1)*50), max(15, abs(v2)*50), v3_thermal/9, v4_matrix*10, v5_mass*18, v6_por*2.5]
    categories = [f'<b>V-TEN:{abs(v1):.1f}</b>', f'<b>MAG:{abs(v2):.1f}</b>', f'<b>K-THR:{v3_thermal:.0f}</b>', 
                  f'<b>C-MAT:{v4_matrix:.1f}</b>', f'<b>R-DEN:{v5_mass:.1f}</b>', f'<b>STRAT:{v6_por:.1f}</b>']
    
    fig_radar = go.Figure(data=go.Scatterpolar(
        r=r_vals, theta=categories, fill='toself', fillcolor='rgba(13, 71, 161, 0.45)', line=dict(color='#0D47A1', width=4)
    ))
    
    fig_radar.update_layout( polar=dict(radialaxis=dict(visible=True, range=[0, 110], gridcolor="#BBB"), angularaxis=dict(tickfont=dict(size=12, color="#0D47A1", family="Arial Black"))), showlegend=False, height=450, margin=dict(l=60, r=60, b=20, t=20), paper_bgcolor='rgba(0,0,0,0)' )
    st.plotly_chart(fig_radar, use_container_width=True)

# LÓGICA DE ALARMA SONORA Y TRANSICIÓN
if sync_score >= 85:
    st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>', unsafe_allow_html=True)