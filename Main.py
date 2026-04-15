Import streamlit as st
import pandas as pd
import numpy as np

# 1. ESTÉTICA DE CONSOLA DE COMANDO (DARK-TECH)
st.set_page_config(page_title="SINCRO-X | ABYSSAL GAS PREDICTOR", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono:wght@300;500&display=swap');
    .stApp { background-color: #020408; color: #00ff41; font-family: 'Roboto Mono', monospace; }
    .stMetric { background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); border: 1px solid #d4af37; border-radius: 5px; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #d4af37; text-transform: uppercase; letter-spacing: 2px; }
    .stSlider { color: #d4af37; }
    .css-10trblm { font-size: 14px; color: #8b949e; } /* Subtítulos */
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO ESTRATÉGICO
st.title("🛡️ SINCRO-X : PROTOCOLO DE GAS PRIMORDIAL")
st.caption("SISTEMA DE ANÁLISIS DE BASAMENTO CRISTALINO | PROYECTO JERICÓ")

# 3. PANELES DE OPERACIÓN
col_control, col_map, col_data = st.columns([1, 2, 1])

with col_control:
    st.subheader("⌨️ INPUT SENSORES")
    # Nombres codificados para protección total de IP
    v1 = st.slider("ANOMALÍA GRAV. BOUGUER (mGal)", -100.0, 100.0, -32.0, help="Diferencial de Masa Volumétrica")
    v2 = st.slider("LINEAMIENTO MAG. (nT/m)", 0.0, 50.0, 12.5, help="Vector de Flujo Estructural")
    v3 = st.slider("GRADIENTE TÉRMICO (°C/km)", 20, 180, 45, help="Energía Endógena de la Singularidad")
    v4 = st.number_input("DENSIDAD DE MATRIZ (g/cm³)", 2.4, 3.2, 2.67)
    v5 = st.checkbox("AUTORIZACIÓN POROSIDAD 1°", value=True)
    
    st.write("---")
    # Lógica de Sincronía Avanzada
    sincronia = (abs(v1) * 0.25) + (v2 * 0.35) + (v3 * 0.8) + (v4 * 2)
    if v5: sincronia += 10
    prob = min(99.8, (sincronia / 1.5))
    
    st.write("**STATUS DEL SISTEMA:**")
    if prob > 85:
        st.success("🟢 OBJETIVO VALIDADO")
    else:
        st.warning("🟡 ESCANEANDO BASAMENTO...")

with col_map:
    st.subheader("🌐 TARGETING: ÁREA 10 KM²")
    # Simulación de coordenadas en el área de interés (ej. cerca a Cartagena/Cuencas Frontera)
    target_lat, target_lon = 10.4, -75.4 
    map_data = pd.DataFrame({'lat': [target_lat], 'lon': [target_lon]})
    st.map(map_data, zoom=12)
    
    if prob > 85:
        st.code(f"COORDENADA DETECTADA:\nLAT: {target_lat}921\nLON: {target_lon}485\nDEPTH: 4,850m (BASEMENT)", language='bash')
    else:
        st.info("AJUSTE SENSORES PARA LOCALIZAR PUNTO DE SINCRONÍA")

with col_data:
    st.subheader("📊 ANALÍTICA")
    # El Predictor de Firma Isotópica (La Bala de Plata)
    iso = -22 + (prob/10) if prob > 50 else -45
    st.metric("FIRMA δ¹³C PROYECTADA", f"{iso:.2f} ‰", delta="PRIMORDIAL" if iso > -20 else "BIÓTICO", delta_color="normal")
    
    st.metric("PRESIÓN DE CABEZAL", f"{v3 * 340:,} PSI")
    st.metric("ENTALPÍA DEL SISTEMA", f"{v3 * 4.8:.1f} kJ/kg")
    
    st.write("---")
    st.write("**LOGOS PREDICTIVE ENGINE**")
    st.caption("V. 3.01 - 2026")

# 4. CIERRE TÉCNICO
st.write("---")
with st.expander("📝 NOTA DE AUTORIDAD TÉCNICA"):
    st.write(f"""
    Este protocolo desestima la teoría biótica tradicional mediante la integración de 5 variables geofísicas. 
    La sincronía de anomalías negativas de masa y lineamientos de sutura tectónica confirman la presencia de 
    Metano Abiótico en el Basamento Cristalino.
    """)
    st.caption("Dr. Edgar Espíndola Niño | Investigador Principal")

Dígame qué hace este software.