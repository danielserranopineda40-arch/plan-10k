<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>10K Runner | Performance Lab</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0a0a0f; --bg2: #111118; --bg3: #1a1a24; --card: #16161f;
    --border: rgba(255,255,255,0.07); --accent: #c8ff3e; --accent2: #ff6b35;
    --accent3: #3ecfff; --accent4: #b06cff; --text: #f0f0f8; --muted: #7b7b96;
    --muted2: #4a4a60; --strength: #ff6b35; --cardio: #3ecfff; --sports: #b06cff; --rest: #c8ff3e;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif; min-height: 100vh; overflow-x: hidden; }
  .wrap { max-width: 1200px; margin: 0 auto; padding: 40px 24px; position: relative; z-index: 1; }

  /* HEADER & CALCULATOR */
  header { margin-bottom: 30px; border-bottom: 1px solid var(--border); padding-bottom: 20px; }
  .pace-calculator { background: var(--card); border: 1px solid var(--accent); border-radius: 20px; padding: 24px; margin-bottom: 40px; }
  .pace-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
  .pace-item { background: var(--bg3); padding: 15px; border-radius: 12px; border: 1px solid var(--border); }
  .pace-val { font-family: 'Syne'; font-size: 1.4rem; font-weight: 800; color: var(--accent); }
  
  input[type="text"] { background: var(--bg); border: 1px solid var(--muted2); color: white; padding: 10px; border-radius: 8px; font-family: 'Syne'; width: 120px; outline: none; }
  input[type="text"]:focus { border-color: var(--accent); }
  .btn-calc { background: var(--accent); color: black; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: transform 0.2s; }
  .btn-calc:active { transform: scale(0.95); }

  /* WEEK NAV */
  .week-nav { display: flex; gap: 8px; margin-bottom: 30px; overflow-x: auto; padding-bottom: 10px; }
  .day-btn { flex-shrink: 0; padding: 12px 18px; border-radius: 15px; border: 1px solid var(--border); background: var(--card); color: var(--muted); cursor: pointer; text-align: center; min-width: 90px; }
  .day-btn.active { background: var(--accent); color: black; border-color: var(--accent); font-weight: bold; }

  /* MAIN GRID */
  .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media(max-width: 900px) { .main-grid { grid-template-columns: 1fr; } }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 24px; }
  .full-span { grid-column: span 2; }
  @media(max-width: 900px) { .full-span { grid-column: span 1; } }

  /* LISTS & ITEMS */
  .exercise-list { list-style: none; display: flex; flex-direction: column; gap: 10px; margin-top: 20px; }
  .exercise-item { display: flex; align-items: center; gap: 12px; padding: 12px; border-radius: 12px; background: var(--bg3); border: 1px solid var(--border); }
  .ex-num { width: 25px; font-weight: 800; color: var(--accent); }
  
  .meals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }
  .meal-block { background: var(--bg3); padding: 15px; border-radius: 12px; border: 1px solid var(--border); }
  .meal-time { font-size: 0.7rem; color: var(--accent); font-weight: bold; text-transform: uppercase; }
  
  .nutri-tip { margin-top: 20px; padding: 20px; border-radius: 15px; background: rgba(200, 255, 62, 0.05); border-left: 4px solid var(--accent); font-style: italic; font-size: 0.9rem; }
</style>
</head>
<body>

<div class="wrap">
  <header>
    <h1 style="font-family: 'Syne'; font-weight: 800; font-size: 2.2rem;">10K<span style="color:var(--accent)">RUNNER</span></h1>
    <p style="color:var(--muted); font-size: 0.9rem;">Plan de Entrenamiento Personalizado - Meta: 24 de Mayo</p>
  </header>

  <section class="pace-calculator">
    <div style="font-family:'Syne'; font-weight:800; margin-bottom:15px;">CALCULADORA DE RITMOS</div>
    <div style="display:flex; flex-wrap:wrap; gap:15px; align-items:center;">
        <div style="display:flex; flex-direction:column; gap:5px;">
            <label style="font-size:0.75rem; color:var(--muted);">TIEMPO OBJETIVO (HH:MM:SS)</label>
            <input type="text" id="targetTime" value="00:50:00">
        </div>
        <button class="btn-calc" onclick="updateDashboard()">ACTUALIZAR PLAN</button>
    </div>
    <div class="pace-grid" id="paceGrid"></div>
  </section>

  <nav class="week-nav" id="weekNav"></nav>
  <div class="main-grid" id="mainGrid"></div>
</div>

<script>
const DAYS = [
  {name:'Lun', date:'27 Abr', type:'strength', title:'Fuerza Funcional'},
  {name:'Mar', date:'28 Abr', type:'cardio', title:'Series de Velocidad'},
  {name:'Mie', date:'29 Abr', type:'rest', title:'Recuperación Activa'},
  {name:'Jue', date:'30 Abr', type:'cardio', title:'Umbral Tempo'},
  {name:'Vie', date:'01 May', type:'strength', title:'Core y Estabilidad'},
  {name:'Sab', date:'02 May', type:'sports', title:'Tirada Larga (Long Run)'},
  {name:'Dom', date:'03 May', type:'rest', title:'Descanso Total'}
];

const PLANS = {
  strength: {
    ex: [{n:'Zancadas', d:'3x12 por pierna'}, {n:'Puente Glúteo', d:'3x15'}, {n:'Plancha', d:'4x45s'}, {n:'Sentadilla Búlgara', d:'3x10'}],
    tip: 'La fuerza evita que tu técnica se desmorone en el km 8.',
    kcal: '2500', prot: '160g', carbs: '280g', fat: '70g',
    meals: [{t:'08:00', n:'Desayuno Proteico', i:['Huevos', 'Avena']}, {t:'14:00', n:'Almuerzo', i:['Pollo', 'Quinoa']}]
  },
  cardio: {
    ex: [{n:'Calentamiento', d:'15min Z2'}, {n:'Series 800m', d:'6 reps (ver ritmos)'}, {n:'Enfriamiento', d:'10min suave'}],
    tip: 'Mantén la hidratación alta. Las series son el motor de tu mejora.',
    kcal: '2800', prot: '140g', carbs: '400g', fat: '60g',
    meals: [{t:'Pre-Entreno', n:'Carga rápida', i:['Plátano', 'Miel']}, {t:'Post', n:'Recuperación', i:['Pasta', 'Atún']}]
  },
  sports: {
    ex: [{n:'Tirada Larga', d:'10-12km ritmo suave'}, {n:'Técnica', d:'5min Skipping'}],
    tip: 'Hoy el objetivo es tiempo en pies, no velocidad. Construye tu base.',
    kcal: '3100', prot: '150g', carbs: '450g', fat: '75g',
    meals: [{t:'Cena Previa', n:'Carga Glucógeno', i:['Pasta', 'Pan']}, {t:'Post', n:'Gran Almuerzo', i:['Carne', 'Arroz']}]
  },
  rest: {
    ex: [{n:'Descanso total', d:'Cero impacto'}, {n:'Movilidad', d:'10min estiramientos'}],
    tip: 'El descanso es donde tus músculos se reparan. ¡No te lo saltes!',
    kcal: '2100', prot: '130g', carbs: '200g', fat: '70g',
    meals: [{t:'Todo el día', n:'Limpieza', i:['Vegetales', 'Frutas', 'Agua']}]
  }
};

let activeDay = 0;

function formatPace(s) {
    const m = Math.floor(s/60); const sec = Math.round(s%60);
    return `${m}:${sec < 10 ? '0' : ''}${sec}`;
}

function updateDashboard() {
    const time = document.getElementById('targetTime').value.split(':');
    const totalSec = (parseInt(time[0])*3600) + (parseInt(time[1])*60) + parseInt(time[2]);
    const racePace = totalSec / 10;

    const paces = [
        {l:'Carrera (10K)', v:racePace}, {l:'Rodaje (Z2)', v:racePace+60},
        {l:'Tempo (Umbral)', v:racePace+15}, {l:'Series (800m)', v:racePace-15}
    ];

    document.getElementById('paceGrid').innerHTML = paces.map(p => `
        <div class="pace-item">
            <div style="font-size:0.7rem; color:var(--muted);">${p.l}</div>
            <div class="pace-val">${formatPace(p.v)} <span style="font-size:0.7rem">min/km</span></div>
        </div>
    `).join('');
    renderDay(activeDay);
}

function buildNav() {
    const nav = document.getElementById('weekNav');
    DAYS.forEach((d, i) => {
        const btn = document.createElement('button');
        btn.className = `day-btn ${i === 0 ? 'active' : ''}`;
        btn.innerHTML = `<div style="font-size:0.7rem">${d.name}</div><div style="font-size:0.9rem">${d.date}</div>`;
        btn.onclick = () => {
            document.querySelectorAll('.day-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeDay = i;
            renderDay(i);
        };
        nav.appendChild(btn);
    });
}

function renderDay(idx) {
    const day = DAYS[idx];
    const plan = PLANS[day.type];
    const grid = document.getElementById('mainGrid');
    grid.innerHTML = `
        <div class="card">
            <h3 class="card-title" style="color:var(--accent)">${day.title}</h3>
            <ul class="exercise-list">
                ${plan.ex.map((e,i) => `<li class="exercise-item"><span class="ex-num">${i+1}</span><div><b>${e.n}</b><br><small style="color:var(--muted)">${e.d}</small></div></li>`).join('')}
            </ul>
            <div class="nutri-tip"><b>Coach Tip:</b> ${plan.tip}</div>
        </div>
        <div class="card">
            <h3 class="card-title">Nutrición & Macros</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:20px;">
                <div class="pace-item"><small>Kcal</small><br><b style="color:var(--accent)">${plan.kcal}</b></div>
                <div class="pace-item"><small>Carbs</small><br><b style="color:var(--cardio)">${plan.carbs}g</b></div>
            </div>
            <div class="meals-grid">
                ${plan.meals.map(m => `<div class="meal-block"><div class="meal-time">${m.t}</div><b>${m.n}</b><br><small>${m.i.join(', ')}</small></div>`).join('')}
            </div>
        </div>
    `;
}

buildNav();
updateDashboard();
</script>
</body>
</html>
