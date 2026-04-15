import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE INTERFAZ PROFESIONAL
st.set_page_config(page_title="SINCRO-X | Gas Primordial", layout="wide")

# Estilo visual oscuro (Dark Mode) para que parezca software de ingeniería
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SINCRO-X: Sistema de Autorización de Perforación")
st.write("---")

# 2. PANEL LATERAL: ENTRADA DE LAS 5 VARIABLES
st.sidebar.header("📊 SENSORES DE CAMPO")
st.sidebar.info("Ajuste los valores detectados por la geofísica:")

# Variable 1: Gravimetría
bouguer = st.sidebar.slider("1. Gravimetría (Bouguer mGal)", -100, 0, -35, help="Objetivo: -15 a -40 mGal")

# Variable 2: Magnetometría
mag = st.sidebar.slider("2. Magnetometría (nT/m)", 0, 20, 8, help="Objetivo: > 5 nT/m")

# Variable 3: Temperatura
temp = st.sidebar.slider("3. Gradiente Térmico (°C/km)", 10, 60, 38, help="Objetivo: > 35 °C/km")

# Variable 4: Densidad de Roca (Dato de Pozo)
rho_b = st.sidebar.number_input("4. Densidad Bulk (g/cm³)", 2.00, 3.00, 2.45, step=0.01)

# Variable 5: Cálculo de Porosidad (Backend integrado)
# Fórmula: Phi = (Matriz - Bulk) / (Matriz - Fluido)
phi = (2.67 - rho_b) / (2.67 - 0.15) * 100
st.sidebar.metric("5. POROSIDAD CALCULADA", f"{phi:.2f} %")

# 3. LÓGICA DE SINCRONÍA (Caja Negra)
score = 0
checks = []

if -40 <= bouguer <= -15:
    score += 25
    checks.append("✅ Anomalía de Masa detectada (Fractura)")
if mag >= 5:
    score += 25
    checks.append("✅ Lineamiento de Sutura confirmado")
if temp >= 35:
    score += 25
    checks.append("✅ Flujo Térmico activo (Gas vivo)")
if phi >= 5:
    score += 25
    checks.append("✅ Porosidad de Reservorio comercial")

# 4. MONITOR PRINCIPAL (Lo que verá el inversor)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Estado de la Sincronía")
    st.metric("PROBABILIDAD DE GAS PRIMORDIAL", f"{score}%")
    
    if score >= 75:
        st.success("🟢 AUTORIZACIÓN: PERFORACIÓN RECOMENDADA")
        st.balloons()
    elif score >= 50:
        st.warning("🟡 ATENCIÓN: REVISIÓN DE DATA REQUERIDA")
    else:
        st.error("🔴 ALERTA: RIESGO ALTO - SINCRONÍA INSUFICIENTE")

with col2:
    st.subheader("Parámetros Críticos de Operación")
    st.markdown(f"""
    * **Presión Estimada:** 15,200 PSI
    * **Temperatura de Fondo:** 232°C
    * **Seguridad:** Reclamo de BOP 15K Mandatorio
    * **Firma Isotópica Esperada:** $\delta^{13}C > -20\%$
    """)

# 5. DIAGNÓSTICO DETALLADO
with st.expander("Ver Diagnóstico Técnico"):
    for c in checks:
        st.write(c)
    if not checks:
        st.write("Sin coincidencias físicas detectadas.")

st.divider()
st.caption("Propiedad Intelectual: Proyecto Jericó | Cartagena 2026")
