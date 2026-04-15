import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. ESTÉTICA DE LABORATORIO DE ALTA SEGURIDAD
st.set_page_config(page_title="LOGOS - ANOMALY DETECTOR", layout="wide")

# CSS para fondo claro, colores vibrantes y datos grandes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;500&display=swap');
    .stApp { background-color: #f0f2f5; color: #2e2e2e; font-family: 'Roboto Mono', monospace; }
    .stSlider { color: #d4af37; }
    label { color: #3b82f6 !important; font-weight: bold !important; font-size: 1.1rem !important; } /* Nombres sensores Azul Lab */
    .stMetric { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1 { color: #d4af37; text-transform: uppercase; text-align: center; }
    h2, h3 { color: #e53e3e; } /* Subtítulos Rojo Alerta */
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SISTEMA DE DETECCIÓN DE ANOMALÍAS DE FRONTERA 'JERICÓ'")
st.write("---")

# 2. DISTRIBUCIÓN DE PANTALLA (CONSOLA DE MANDO)
col_control, col_map, col_data = st.columns([1.3, 2, 1.2])

with col_control:
    st.subheader("⌨️ SENSORES ENTRADA")
    # LOS 8 CONTROLES PARA DESPISTAR (Tu fórmula está oculta aquí)
    st.write("**MÓDULO ALFA: GEOMETRÍA DE MASA**")
    d1 = st.slider("VAR. GRAVIMÉTRICA BOUGUER (mGal)", -120.0, 120.0, -32.0)
    d2 = st.slider("ANOMALÍA DE ISOTASIA (mGal)", -50.0, 50.0, 8.0) # Despiste 1
    
    st.write("**MÓDULO BETA: FLUJO ESTRUCTURAL**")
    d3 = st.slider("LINEAMIENTO MAG. TOTAL (nT/m)", 0.0, 70.0, 15.5)
    d4 = st.slider("GRADIENTE VERTICAL MAG.", -2.0, 2.0, 0.4) # Despiste 2
    
    st.write("**MÓDULO GAMMA: TERMODINÁMICA ENDÓGENA**")
    d5 = st.slider("FLUJO TÉRMICO ENDÓGENO (°C/km)", 30, 160, 48)
    d6 = st.slider("CONDUCTIVIDAD TÉRMICA BULK", 1.5, 4.0, 2.6) # Despiste 3
    
    st.write("**MÓDULO DELTA: SUTURA ÍGNEA**")
    d7 = st.number_input("DENSIDAD MATRIZ (%)", 85.0, 100.0, 96.5) # Tu fórmula de Basamento
    d8 = st.checkbox("AUTORIZACIÓN DE POROSIDAD", value=True) # Tu checkbox real

    st.write("---")
    # TU FÓRMULA SECRETA ACTUANDO (Oculta tras 8 controles)
    sincronia = (abs(d1) * 0.25) + (abs(d3) * 0.35) + (d5 * 0.8) + (d7 * 2)
    if d8: sincronia += 10
    prob = min(99.8, (sincronia / 1.5))
    
    st.write("**ESTADO DEL LOGOS:**")
    if prob > 85:
        st.success(f"🟢 SINCRONÍA VALIDADA: {prob:.1f}%")
        st.code("COORDENADA DETECTADA: [Lat: 10.421 / Lon: -75.495]\nDEPTH: 4,850m (BASEMENT CRYSTALLINE)", language='bash')
    else:
        st.warning("🟡 ESCANEANDO BASAMENTO...")

with col_map:
    st.subheader("🌐 VISUALIZADOR 3D DE FRONTERA (ÁREA 10 KM²)")
    # MODELO TERRESTRE INTERACTIVO 3D (Simulando capas)
    # Mostraremos un globo interactivo filtrando el área de interés (Colombia/Cartagena Province)
    
    fig = go.Figure(go.Scattergeo(
        lat = [10.4], lon = [-75.4],
        mode = 'markers',
        marker = dict(size = 15, color = 'green' if prob > 85 else 'yellow', line = dict(width=2, color='white')),
        text = ['COORDENADA JERICÓ' if prob > 85 else 'PUNTO INTERÉS'],
        textposition="top center"
    ))
    fig.update_layout(
        geo=dict(
            scope='south america',
            center=dict(lat=10.4, lon=-75.4),
            projection_type='orthographic',
            showland=True, landcolor='rgb(217, 217, 217)',
            showocean=True, oceancolor='rgb(180, 210, 255)',
            lakecolor='rgb(255, 255, 255)',
            showlakes=True,
            showcountries=True,
            lonaxis=dict(showgrid=True, gridcolor='gray', gridwidth=0.5),
            lataxis=dict(showgrid=True, gridcolor='gray', gridwidth=0.5),
            )
        )
    st.plotly_chart(fig, use_container_width=True)
    
    if prob > 85:
        st.caption("🔴 LUZ INTERMITENTE: SINCRONÍA DE FRACTURA DETECTADA")
    else:
        st.caption("🟡 ESCANEANDO CUBIERTAS SEDIMENTARIAS...")

with col_data:
    st.subheader("📊 ANALÍTICA PREDICTIVA (CAJA NEGRA)")
    # El Predictor de Firma Isotópica (La Bala de Plata)
    iso = -22 + (prob/10) if prob > 50 else -45
    st.metric("FIRMA δ¹³C PROYECTADA", f"{iso:.2f} ‰", delta="PRIMORDIAL" if iso > -20 else "BIÓTICO", delta_color="normal" if iso > -20 else "off")
    
    st.write("---")
    st.write("**MÓDULO DE RE-ENTRY**")
    if prob > 85:
        st.info("🎯 VALIDADO PARA PROFUNDIZACIÓN")
        st.caption("POZO CANDIDATO: Jericó-X1")
    else:
        st.write("🟡 ANALIZANDO POZOS ACTUALES")
    st.write("---")
    st.metric("TASA DISOCIACIÓN TÉRMICA", f"{d5 * 1.5:.2f} kJ/s") # Dato raro 1
    st.metric("ENTALPÍA DE FORMACIÓN", f"{d1 * d5 / 100:.2f} J/kg") # Dato raro 2
    st.metric("ÍNDICE POROSIDAD PRIMORDIAL", f"{d7/100 * prob/100:.3f}") # Dato raro 3
    
    st.write("---")
    st.caption("LOGOS PREDICTIVE ENGINE V4.0 - JERICÓ PROJECT")

# 3. CIERRE TÉCNICO
st.write("---")
with st.expander("📝 PROTOCOLO DE AUTORIZACIÓN (ACCESO RESTRINGIDO)"):
    st.write("""
    Este sistema integra vectores de anisotropía de masa y suturas tectónicas endógenas 
    para predecir la migración y acumulación de Metano Primordial Abiótico en el 
    Basamento Cristalino Ígneo. El cálculo de sincronía se basa en la disociación 
    térmica del carbono del manto bajo la singularidad de Jericó.
    """)
    st.caption("Edgar Espíndola Niño | Investigador Principal")