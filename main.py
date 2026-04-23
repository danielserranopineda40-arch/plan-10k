import streamlit as st
from datetime import date, timedelta

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Running 10K Pro", page_icon="🏃‍♂️", layout="wide")

# Inicializar el registro de progreso si no existe
if 'completados' not in st.session_state:
    st.session_state.completados = {}

# 2. BASE DE DATOS DEL PLAN (Semanas de entrenamiento)
# Puedes expandir este diccionario con todas las fechas hasta el 24 de mayo
plan_entrenamiento = {
    "2026-04-22": "Trote Suave (5 km) - Ritmo regenerativo",
    "2026-04-23": "Tempo Run (6 km) - Ritmo 5:30 min/km",
    "2026-04-24": "Descanso Total - Estiramientos",
    "2026-04-25": "Carrera Larga (10 km) - Base aeróbica",
    "2026-04-26": "Caminata activa (30 min)",
    "2026-04-27": "Series (5x400m) - Velocidad alta",
}

# 3. CONTENIDO DE DIETAS
dietas_ejemplo = {
    "Día de Entrenamiento Suave": {
        "Desayuno": "Avena con leche vegetal, canela y medio banano.",
        "Almuerzo": "Pechuga de pollo a la plancha, 1 taza de arroz integral y brócoli al vapor.",
        "Cena": "Omelet de 2 huevos con espinacas y una tostada integral.",
        "Snack Pre-Run": "Una manzana o un puñado de almendras."
    },
    "Día de Carrera Larga/Intensa": {
        "Desayuno": "Tostadas con aguacate y huevo poché + zumo de naranja.",
        "Almuerzo": "Pasta integral boloñesa (carne magra) y ensalada verde.",
        "Cena": "Filete de pescado blanco (merluza/lenguado) con puré de camote (batata).",
        "Snack Pre-Run": "Pan blanco con miel o mermelada (energía rápida)."
    }
}

# --- INTERFAZ DE USUARIO ---
st.title("🏃‍♂️ Mi Panel de Control 10K")

# Sidebar para métricas rápidas
with st.sidebar:
    st.header("📊 Tu Progreso")
    total_dias = len(plan_entrenamiento)
    hechos = sum(st.session_state.completados.values())
    porcentaje = hechos / total_dias if total_dias > 0 else 0
    
    st.metric("Completados", f"{hechos}/{total_dias}")
    st.progress(porcentaje)
    st.write(f"Has cumplido el {int(porcentaje*100)}% del plan.")

# DIVISION POR PESTAÑAS
tab_hoy, tab_plan, tab_dieta = st.tabs(["🚀 Hoy", "📅 Plan Completo", "🥗 Nutrición Detallada"])

# TAB 1: HOY
with tab_hoy:
    hoy_str = str(date.today())
    st.subheader(f"Entrenamiento para hoy ({hoy_str})")
    
    if hoy_str in plan_entrenamiento:
        tarea = plan_entrenamiento[hoy_str]
        col_t, col_b = st.columns([3, 1])
        col_t.info(f"### {tarea}")
        
        if col_b.button("¡Hecho! ✅", key="btn_hoy"):
            st.session_state.completados[hoy_str] = True
            st.balloons()
    else:
        st.warning("No hay un entrenamiento específico programado para hoy en la base de datos.")

# TAB 2: PLAN COMPLETO
with tab_plan:
    st.subheader("Calendario de Entrenamiento")
    st.write("Haz clic en cada día para ver detalles y registrar tu avance.")
    
    for fecha, actividad in plan_entrenamiento.items():
        with st.expander(f"{'✅' if st.session_state.completados.get(fecha) else '⏳'} {fecha}"):
            st.write(f"**Actividad:** {actividad}")
            check = st.checkbox("Marcar como completado", key=f"check_{fecha}", 
                                value=st.session_state.completados.get(fecha, False))
            st.session_state.completados[fecha] = check

# TAB 3: DIETAS Y EJEMPLOS
with tab_dieta:
    st.subheader("Plan de Alimentación Sugerido")
    
    tipo_dia = st.radio("Selecciona tu tipo de día:", ["Día de Entrenamiento Suave", "Día de Carrera Larga/Intensa"])
    
    dieta = dietas_ejemplo[tipo_dia]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"🌅 **Desayuno:** {dieta['Desayuno']}")
        st.markdown(f"☀️ **Almuerzo:** {dieta['Almuerzo']}")
    with c2:
        st.markdown(f"🍎 **Snack:** {dieta['Snack Pre-Run']}")
        st.markdown(f"🌙 **Cena:** {dieta['Cena']}")
    
    st.divider()
    st.info("💡 **Consejo Pro:** No olvides beber al menos 2.5 litros de agua al día y añadir electrolitos si tu entrenamiento dura más de 60 minutos.")
