import streamlit as st
from datetime import date, timedelta

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Plan 10K - Lavamasters", page_icon="🏃‍♂️", layout="wide")

if 'completados' not in st.session_state:
    st.session_state.completados = {}

# 2. GENERADOR AUTOMÁTICO DEL PLAN HASTA EL 24 DE MAYO
def generar_plan_completo():
    fecha_inicio = date(2026, 4, 22)
    fecha_meta = date(2026, 5, 24)
    plan = {}
    
    delta = fecha_meta - fecha_inicio
    for i in range(delta.days + 1):
        dia_actual = fecha_inicio + timedelta(days=i)
        dia_semana = dia_actual.weekday() # 0=Lunes, 6=Domingo
        fecha_str = str(dia_actual)
        
        # Lógica de entrenamiento por día de la semana
        if dia_semana == 0: # Lunes
            plan[fecha_str] = {"tipo": "Fuerza + Trote", "actividad": "40 min Trote suave", "fuerza": ["Sentadillas: 3x15", "Plancha: 3x60 seg", "Zancadas: 3x12"], "sprints": "No toca"}
        elif dia_semana == 1: # Martes
            plan[fecha_str] = {"tipo": "Velocidad", "actividad": "Calentamiento 15 min + Sprints", "fuerza": ["Plancha lateral: 2x30 seg"], "sprints": "6 Sprints de 100m (90% esfuerzo)"}
        elif dia_semana == 2: # Miércoles
            plan[fecha_str] = {"tipo": "Descanso", "actividad": "Descanso activo / Estiramientos", "fuerza": [], "sprints": "No toca"}
        elif dia_semana == 3: # Jueves
            plan[fecha_str] = {"tipo": "Tempo", "actividad": "6 km a ritmo de carrera", "fuerza": ["Puente de glúteo: 3x20", "Flexiones: 3x10"], "sprints": "No toca"}
        elif dia_semana == 4: # Viernes
            plan[fecha_str] = {"tipo": "Fuerza", "actividad": "Enfoque total en Core", "fuerza": ["Plancha: 4x60 seg", "Burpees: 3x10"], "sprints": "No toca"}
        elif dia_semana == 5: # Sábado
            km = 8 if i < 15 else 10 # Aumenta la distancia según se acerca la meta
            plan[fecha_str] = {"tipo": "Fondo", "actividad": f"Carrera Larga ({km} km)", "fuerza": [], "sprints": "No toca"}
        else: # Domingo
            plan[fecha_str] = {"tipo": "Descanso", "actividad": "Descanso Total", "fuerza": [], "sprints": "No toca"}
            
    # Caso especial: Día de la carrera
    plan["2026-05-24"] = {"tipo": "🏁 META", "actividad": "CARRERA 10K - ¡A por el tiempo objetivo!", "fuerza": [], "sprints": "¡Todo el esfuerzo aquí!"}
    return plan

plan_entrenamiento = generar_plan_completo()

# --- INTERFAZ ---
st.title("🏃‍♂️ Mi Plan 10K Personalizado")

# Métricas de la barra lateral
hoy = date.today()
meta = date(2026, 5, 24)
dias_faltan = (meta - hoy).days
st.sidebar.header("📊 Resumen")
st.sidebar.metric("Días para la carrera", f"{max(0, dias_faltan)}")

hechos = sum(st.session_state.completados.values())
st.sidebar.write(f"Entrenamientos completados: **{hechos}**")

tab_hoy, tab_plan, tab_dieta = st.tabs(["🚀 Hoy", "📅 Calendario Completo", "🥗 Nutrición"])

# PESTAÑA HOY
with tab_hoy:
    hoy_str = str(hoy)
    if hoy_str in plan_entrenamiento:
        dia = plan_entrenamiento[hoy_str]
        st.info(f"### {dia['tipo']}: {dia['actividad']}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 💪 Rutina de Fuerza")
            if dia['fuerza']:
                for f in dia['fuerza']: st.write(f"✅ {f}")
            else: st.write("Hoy es día de descanso muscular.")
            
        with c2:
            st.markdown("#### ⚡ Velocidad/Sprints")
            st.write(dia['sprints'])

        if st.button("Marcar como completado ✅"):
            st.session_state.completados[hoy_str] = True
            st.balloons()
    else:
        st.success("¡Felicidades! Si no hay plan, es que ya cruzaste la meta o estás fuera de fechas.")

# PESTAÑA PLAN COMPLETO (Ahora muestra todos los días)
with tab_plan:
    st.subheader("Tu camino al 24 de Mayo")
    for fecha, datos in plan_entrenamiento.items():
        listo = st.session_state.completados.get(fecha, False)
        with st.expander(f"{'✅' if listo else '⏳'} {fecha} - {datos['tipo']}"):
            st.write(f"**Actividad:** {datos['actividad']}")
            if datos['fuerza']: st.write(f"**Fuerza:** {', '.join(datos['fuerza'])}")
            
            check = st.checkbox("Completado", key=f"check_{fecha}", value=listo)
            st.session_state.completados[fecha] = check

# PESTAÑA DIETA
with tab_dieta:
    st.subheader("Ejemplos de alimentación")
    st.markdown("""
    **Día de entrenamiento:**
    * **Desayuno:** Avena con banano y miel (Energía).
    * **Almuerzo:** Pechuga de pollo, arroz y aguacate.
    * **Cena:** Pescado o huevos con ensalada verde.
    
    **Día de descanso:**
    * Reducir carbohidratos (menos arroz/pasta), aumentar proteínas y fibra.
    """)
