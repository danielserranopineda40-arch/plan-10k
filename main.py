import streamlit as st
from datetime import date

# Configuración
st.set_page_config(page_title="Mi Plan 10K", page_icon="🏃‍♂️")

st.title("🏃‍♂️ Objetivo: 10K - 24 de Mayo")

# Lógica de fechas
hoy = date.today()
meta = date(2026, 5, 24)
dias_restantes = (meta - hoy).days

st.metric("Días para la carrera", f"{max(0, dias_restantes)} días")

# Base de datos del plan
plan = {
    "2026-04-22": "Trote Suave (5 km) - ¡Empezamos!",
    "2026-04-23": "Tempo Run (6 km) - Ritmo constante",
    "2026-04-24": "Descanso total - Hidratación",
    "2026-04-25": "Carrera Larga (10 km) - Ritmo suave",
}

fecha_str = str(hoy)

st.header("📋 Entrenamiento de Hoy")
if fecha_str in plan:
    st.success(f"**{plan[fecha_str]}**")
else:
    st.info("Hoy toca seguir el ritmo base o descanso activo.")

# Pestañas
tab1, tab2, tab3 = st.tabs(["💪 Fuerza", "⚡ Técnica", "🥗 Dieta"])
with tab1:
    st.write("- Sentadillas: 15 reps\n- Plancha: 60 seg")
with tab2:
    st.write("Enfoque en caer con el medio pie.")
with tab3:
    st.write("Carbohidratos antes, proteína después.")
