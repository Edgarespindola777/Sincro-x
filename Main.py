import streamlit as st

# 1. CONFIGURACIÓN PROFESIONAL
st.set_page_config(page_title="SINCRO-X | Gas Primordial", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    iframe { border-radius: 15px; border: 2px solid #4ade80; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SINCRO-X: Sistema de Autorización de Perforación")
st.write("---")

# 2. PANEL DE CONTROL
st.sidebar.header("📊 SENSORES DE CAMPO")
grav = st.sidebar.slider("1. Gravimetría (Bouguer mGal)", -150, 150, 35)
magnet = st.sidebar.slider("2. Magnetometría (nT/m)", -50, 50, 8)
gradiente = st.sidebar.slider("3. Gradiente Térmico (°C/km)", 10, 100, 38)
densidad = st.sidebar.number_input("4. Densidad Bulk (g/cm³)", 1.0, 3.0, 2.45)
porosidad = st.sidebar.checkbox("5. Evidencia de Porosidad Primaria", True)

sincronia = (abs(grav) * 0.2) + (abs(magnet) * 0.3) + (gradiente * 1.5) + (densidad * 10)
if porosidad: sincronia += 20

# 3. INTERFAZ TÉCNICA
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Estado de la Sincronía (Visualización Térmica)")
    # VIDEO TÉCNICO DE YOUTUBE
    st.video("https://www.youtube.com/watch?v=J3mC8-9_WvA") 
    
    if sincronia > 80:
        st.success("🟢 AUTORIZACIÓN: PERFORACIÓN RECOMENDADA")
    else:
        st.warning("🟡 ANALIZANDO SINCRONÍA...")

with col2:
    st.subheader("Parámetros Críticos")
    st.metric("Presión Estimada", "15,200 PSI")
    st.metric("Temperatura de Fondo", "232°C")
    st.metric("Firma Isotópica δ¹³C", "> -20‰")
    st.info("✅ Sistema Protegido: Proyecto Jericó")

with st.expander("🔬 Ver Diagnóstico Técnico"):
    st.write(f"Puntaje de Sincronía: {sincronia:.2f}. Basado en el Modelo de Nucleosíntesis Térmica del Carbón.")