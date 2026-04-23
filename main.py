import streamlit as st
from datetime import date

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Running 10K Pro", page_icon="🏃‍♂️", layout="wide")

if 'completados' not in st.session_state:
    st.session_state.completados = {}

# 2. BASE DE DATOS AMPLIADA (Entrenamiento + Fuerza + Sprints)
plan_entrenamiento = {
    "2026-04-22": {
        "tipo": "Carrera",
        "actividad": "Trote Suave (5 km)",
        "fuerza": ["Sentadillas: 3x15", "Plancha: 3x60 seg", "Puente de glúteo: 3x15"],
        "tecnica": "Enfoque en postura erguida"
    },
    "2026-04-23": {
        "tipo": "Velocidad",
        "actividad": "Tempo Run (6 km)",
        "sprints": "4 Sprints de 100m (al 90% esfuerzo)",
        "fuerza": ["Zancadas: 3x12 por pierna", "Plancha lateral: 2x30 seg por lado"]
    },
    "2026-04-24": {
        "tipo": "Descanso",
        "actividad": "Descanso Total / Movilidad articular",
        "fuerza": [],
        "tecnica": ""
    },
    "2026-04-25": {
        "tipo": "Fondo",
        "actividad": "Carrera Larga (10 km)",
        "fuerza": ["Plancha: 2x60 seg (post-carrera)"],
        "tecnica": "Cadencia estable (170-180 ppm)"
    }
}

# 3. DIETAS
dietas = {
    "Día de Entrenamiento": "**Desayuno:** Avena con banano. **Almuerzo:** Pollo con arroz integral. **Cena:** Omelet con espinaca. **Snack:** Manzana.",
    "Día de Descanso": "**Desayuno:** Huevos revueltos. **Almuerzo:** Pescado con ensalada. **Cena:** Yogur griego con nueces."
}

# --- INTERFAZ ---
st.title("🏃‍♂️ Plan 10K: Hacia el 24 de Mayo")

tab_hoy, tab_plan, tab_dieta = st.tabs(["🚀 Hoy", "📅 Plan Completo", "🥗 Nutrición"])

# TAB 1: HOY (CON DETALLES DE FUERZA Y SPRINTS)
with tab_hoy:
    hoy_str = str(date.today())
    if hoy_str in plan_entrenamiento:
        dia = plan_entrenamiento[hoy_str]
        st.subheader(f"Objetivo de hoy: {dia['actividad']}")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("### 🏃 Cardio")
            st.write(dia['actividad'])
            if "sprints" in dia:
                st.warning(f"⚡ **Sprints:** {dia['sprints']}")
        
        with c2:
            st.markdown("### 💪 Fuerza & Core")
            if dia['fuerza']:
                for ex in dia['fuerza']:
                    st.write(f"- {ex}")
            else:
                st.write("Día de recuperación muscular.")
        
        with c3:
            st.markdown("### 🛠️ Técnica")
            st.write(dia.get('tecnica', "Enfoque en respiración nasal."))

        if st.button("Marcar entrenamiento completo ✅"):
            st.session_state.completados[hoy_str] = True
            st.balloons()
    else:
        st.info("No hay entrenamiento programado para hoy. ¡Aprovecha para descansar!")

# TAB 2: PLAN COMPLETO
with tab_plan:
    st.subheader("Historial y Futuro")
    for fecha, datos in plan_entrenamiento.items():
        hecho = st.session_state.completados.get(fecha, False)
        with st.expander(f"{'✅' if hecho else '⏳'} {fecha} - {datos['tipo']}"):
            st.write(f"**Principal:** {datos['actividad']}")
            if datos['fuerza']:
                st.write(f"**Fuerza:** {', '.join(datos['fuerza'])}")
            if "sprints" in datos:
                st.write(f"**Velocidad:** {datos['sprints']}")
            
            check = st.checkbox("Completado", key=f"check_{fecha}", value=hecho)
            st.session_state.completados[fecha] = check

# TAB 3: DIETAS
with tab_dieta:
    st.subheader("Guía de Alimentación")
    tipo = st.selectbox("¿Cómo es tu día hoy?", ["Día de Entrenamiento", "Día de Descanso"])
    st.info(dietas[tipo])
    
    st.markdown("""
    ---
    ### 💡 Tips para las Planchas:
    * **Espalda recta:** No dejes caer la cadera.
    * **Respiración:** No aguantes el aire, respira constante.
    * **Sprints:** Camina de regreso al punto de inicio para recuperar antes del siguiente.
    """)
