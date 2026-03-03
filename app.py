import streamlit as st
from streamlit_lottie import st_lottie
import json
import joblib
import pandas as pd
import os
import plotly.graph_objects as go
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Json configuration
# ─────────────────────────────────────────────────────────────
HISTORY_FILE = "./assets/history.json"

def load_history() -> list:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_history(new_record: dict) -> None:
    existing = load_history()
    existing.insert(0, new_record)
    existing = existing[:50]
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Academic Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ─────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
    --navy:       #0F172A;
    --slate:      #1E293B;
    --slate-md:   #334155;
    --gold:       #F59E0B;
    --gold-light: #FCD34D;
    --gold-dim:   rgba(245, 158, 11, 0.15);
    --gold-glow:  rgba(245, 158, 11, 0.35);
    --text:       #E2E8F0;
    --text-dim:   #94A3B8;
    --glass:      rgba(30, 41, 59, 0.7);
    --glass-border: rgba(245, 158, 11, 0.2);
    --radius:     16px;
    --radius-sm:  10px;
}

html, body, [data-testid="stAppViewContainer"], .main {
    background: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, rgba(245,158,11,0.06) 1px, transparent 1px);
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    background: transparent !important;
    padding-top: 2rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--gold) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
    margin: 1.2rem 0 !important;
    opacity: 0.45;
}

/* Inputs */
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stTextInput input {
    background: var(--slate) !important;
    border: 1px solid var(--slate-md) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] .stNumberInput input:focus,
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}

/* Button */
.stButton > button {
    background: var(--gold) !important;
    color: var(--navy) !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 12px 18px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px var(--gold-glow) !important;
}
.stButton > button:hover {
    background: var(--gold-light) !important;
    transform: translateY(-1px) !important;
}

/* Cards */
div[data-testid="column"] {
    background: var(--glass) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius) !important;
    padding: 22px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    color: var(--gold) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--slate-md); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* Hide sidebar collapse */
[data-testid="collapsedControl"],
button[kind="header"],
[data-testid="stSidebarCollapseButton"] {
    display: none !important;
    visibility: hidden !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def load_lottiefile(filepath: str):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@st.cache_resource
def load_selected_model(model_filename: str):
    """
    Robusto: busca el modelo en varios lugares típicos:
    - ./models/<file>
    - ./notebooks/<file>
    - ./notebooks/models/<file>
    - ./<file>
    """
    candidates = [
        model_filename,
        os.path.join("models", model_filename),
        os.path.join("notebooks", model_filename),
        os.path.join("notebooks", "models", model_filename),
    ]
    for path in candidates:
        if os.path.exists(path):
            return joblib.load(path)
    return None


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = load_history()[:8]
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding: 8px 0 18px 0;">
            <div style="font-size:5.8rem; line-height:1;">🎓</div>
            <div style="font-weight:800; font-size:2.05rem; color:#F59E0B; margin-top:6px;">
                Academic Predictor
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
        <div style="font-size:1.1rem;color:#94A3B8;text-transform:uppercase;
                    letter-spacing:0.1em;font-weight:700;margin-bottom:8px;">
            Modelo de predicción
        </div>
    """, unsafe_allow_html=True)

    tipo_modelo = st.radio(
        "Modelo",
        options=["Completo", "Básico"],
        label_visibility="collapsed",
        horizontal=True
    )

    st.markdown("---")

    st.markdown("""
        <div style="font-size:1.1rem;color:#94A3B8;text-transform:uppercase;
                    letter-spacing:0.1em;font-weight:700;margin-bottom:12px;">
            Datos del estudiante
        </div>
    """, unsafe_allow_html=True)

    # Rangos más razonables (sin romper el modelo)
    horas_estudio = st.slider("📚 Horas de estudio", 0, 24, 5)
    promedio_anterior = st.slider("📊 Promedio anterior", 0, 100, 70)

    if tipo_modelo == "Completo":
        horas_sueno = st.slider("😴 Horas de sueño", 0, 12, 7)
        examenes_practica = st.slider("📝 Exámenes de práctica", 0, 50, 2)

        # ✅ Toggle en vez de selectbox
        # (st.toggle existe en Streamlit moderno; si no, fallback a checkbox)
        try:
            extracurriculares_bool = st.toggle("🎯 Actividades extracurriculares", value=False)
        except Exception:
            extracurriculares_bool = st.checkbox("🎯 Actividades extracurriculares", value=False)

        extra_val = 1 if extracurriculares_bool else 0
        datos_para_df = [horas_estudio, promedio_anterior, extra_val, horas_sueno, examenes_practica]
    else:
        datos_para_df = [horas_estudio, promedio_anterior]

    st.markdown("---")

    predict_btn = st.button("⚡ Predecir rendimiento", use_container_width=True)
    save_btn = st.button("💾 Guardar predicción", use_container_width=True)

    st.markdown(f"""
        <div style="
            margin-top:14px;
            background:rgba(245,158,11,0.08);
            border:1px solid rgba(245,158,11,0.2);
            border-radius:10px;
            padding:10px 14px;
            font-size:0.95rem;
            color:#94A3B8;
            text-align:center;
        ">
            Modelo activo<br>
            <span style="color:#F59E0B;font-weight:800;">
                {'✦ Completo' if tipo_modelo == 'Completo' else '◈ Básico'}
            </span>
        </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
if tipo_modelo == "Completo":
    model = load_selected_model("modelo_multiple.pkl")
    columnas_modelo = [
        "Hours Studied",
        "Previous Scores",
        "Extracurricular Activities",
        "Sleep Hours",
        "Sample Question Papers Practiced",
    ]
else:
    model = load_selected_model("modelo_notas.pkl")
    columnas_modelo = ["Hours Studied", "Previous Scores"]


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
lottie_robot = load_lottiefile("assets/niu.json")
badge_color = "#F59E0B" if tipo_modelo == "Completo" else "#38BDF8"
badge_label = "Modelo Completo" if tipo_modelo == "Completo" else "Modelo Básico"

st.markdown(f"""
<div style="text-align:center; padding: 10px 0 26px 0;">
    <div style="display:inline-block; margin-bottom:12px;">
        <span style="
            background: rgba(245,158,11,0.12);
            border: 1px solid rgba(245,158,11,0.35);
            color: {badge_color};
            font-size:0.95rem;
            font-weight:800;
            letter-spacing:0.1em;
            text-transform:uppercase;
            padding:5px 14px;
            border-radius:20px;
        ">{badge_label}</span>
    </div>

    <h1 style="
        font-weight:800;
        font-size:clamp(2.3rem, 4vw, 3.4rem);
        color:#E2E8F0;
        letter-spacing:-0.03em;
        margin:0 0 8px 0;
        line-height:1.1;
    ">Predictor de Rendimiento<br>
        <span style="color:#F59E0B;">Académico</span>
    </h1>

    <p style="
        color:#94A3B8;
        font-size:1.15rem;
        margin:0;
        max-width:560px;
        margin-inline:auto;
    ">
        Introduce los datos en el panel izquierdo y pulsa <strong style="color:#F59E0B;">Predecir</strong>.
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────────────────────
if predict_btn:
    if model is None:
        st.error("⚠️ No se pudo cargar el modelo. Revisa la ruta del archivo .pkl.")
    else:
        df_input = pd.DataFrame([datos_para_df], columns=columnas_modelo)
        try:
            prediction = float(model.predict(df_input)[0])
            prediction = max(0.0, min(100.0, prediction))

            nivel = "Alto" if prediction >= 70 else ("Medio" if prediction >= 45 else "Bajo")
            nivel_color  = "#22C55E" if prediction >= 70 else ("#F59E0B" if prediction >= 45 else "#EF4444")
            nivel_bg     = "rgba(34,197,94,0.1)"  if prediction >= 70 else ("rgba(245,158,11,0.1)" if prediction >= 45 else "rgba(239,68,68,0.1)")
            nivel_border = "rgba(34,197,94,0.3)"  if prediction >= 70 else ("rgba(245,158,11,0.3)" if prediction >= 45 else "rgba(239,68,68,0.3)")

            st.session_state.last_prediction = {
                "score": round(prediction, 1),
                "modelo": tipo_modelo,
                "horas": horas_estudio,
                "prev": promedio_anterior,
                "nivel": nivel,
                "nivel_color": nivel_color,
                "nivel_bg": nivel_bg,
                "nivel_border": nivel_border,
                "datos_para_df": datos_para_df,
                "columnas_modelo": columnas_modelo,
                "coef": getattr(model, "coef_", []).tolist() if hasattr(model, "coef_") else [],
                "intercept": float(getattr(model, "intercept_", 0.0)),
            }
        except Exception as e:
            st.error(f"⚠️ Error en la predicción: {e}")


# ─────────────────────────────────────────────────────────────
# SAVE HISTORY
# ─────────────────────────────────────────────────────────────
if save_btn and st.session_state.last_prediction:
    lp = st.session_state.last_prediction
    new_record = {
        "score": lp["score"],
        "modelo": lp["modelo"],
        "horas": lp["horas"],
        "prev": lp["prev"],
        "nivel": lp["nivel"],
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    save_history(new_record)
    st.session_state.history.insert(0, new_record)
    st.session_state.history = st.session_state.history[:8]


# ─────────────────────────────────────────────────────────────
# MAIN VIEW
# ─────────────────────────────────────────────────────────────
if st.session_state.last_prediction:
    lp = st.session_state.last_prediction
    prediction = lp["score"]
    nivel = lp["nivel"]
    nivel_color = lp["nivel_color"]
    nivel_bg = lp["nivel_bg"]
    nivel_border = lp["nivel_border"]
    c = lp["coef"]
    i = lp["intercept"]

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid rgba(245,158,11,0.3);
        border-radius: 20px;
        padding: 34px 36px;
        text-align: center;
        margin-bottom: 24px;
        position: relative; overflow: hidden;">
        <div style="position:absolute;top:-50px;left:50%;transform:translateX(-50%);
            width:300px;height:300px;
            background:radial-gradient(circle,rgba(245,158,11,0.08) 0%,transparent 70%);
            pointer-events:none;"></div>
        <div style="color:#94A3B8;font-size:0.78rem;text-transform:uppercase;
            letter-spacing:0.12em;font-weight:800;margin-bottom:10px;">
            Performance Index Estimado</div>
        <div style="font-family:'DM Mono',monospace;font-size:clamp(3.3rem,8vw,5.6rem);
            font-weight:700;color:#F59E0B;line-height:1;margin-bottom:14px;">
            {prediction}<span style="font-size:0.35em;color:#475569;">/100</span></div>
        <span style="background:{nivel_bg};border:1px solid {nivel_border};
            color:{nivel_color};font-size:0.82rem;font-weight:800;
            letter-spacing:0.08em;text-transform:uppercase;
            padding:5px 16px;border-radius:20px;">● Rendimiento {nivel}</span>
    </div>
    """, unsafe_allow_html=True)

    met1, met2, met3 = st.columns(3)
    with met1: st.metric("Horas de estudio", f"{lp['horas']}h")
    with met2: st.metric("Promedio anterior", f"{lp['prev']}/100")
    with met3: st.metric("Score estimado", f"{prediction:.0f} pts")

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2, gap="medium")
    DARK_BG = "rgba(0,0,0,0)"
    GRID_COLOR = "rgba(255,255,255,0.05)"
    FONT_COLOR = "#94A3B8"
    GOLD = "#F59E0B"

    with col_g1:
        st.markdown('<div style="font-size:0.78rem;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;font-weight:800;margin-bottom:12px;">Importancia de variables</div>', unsafe_allow_html=True)

        if c and len(c) == len(lp["columnas_modelo"]):
            df_pesos = pd.DataFrame({"Variable": lp["columnas_modelo"], "Impacto": c}).sort_values("Impacto", ascending=True)
            colors_bar = [GOLD if v >= 0 else "#EF4444" for v in df_pesos["Impacto"]]
            fig_bar = go.Figure(go.Bar(
                x=df_pesos["Impacto"],
                y=df_pesos["Variable"],
                orientation="h",
                marker_color=colors_bar,
                marker_line_width=0
            ))
            fig_bar.update_layout(
                paper_bgcolor=DARK_BG,
                plot_bgcolor=DARK_BG,
                font=dict(family="DM Sans", color=FONT_COLOR, size=12),
                margin=dict(l=0, r=0, t=10, b=0),
                height=280,
                xaxis=dict(gridcolor=GRID_COLOR, zeroline=True, zerolinecolor="rgba(255,255,255,0.1)"),
                yaxis=dict(gridcolor=GRID_COLOR),
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No hay coeficientes disponibles para mostrar (modelo sin coef_).")

    with col_g2:
        st.markdown('<div style="font-size:0.78rem;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;font-weight:800;margin-bottom:12px;">Nivel de rendimiento</div>', unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            number=dict(font=dict(family="DM Mono", color=GOLD, size=42)),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=FONT_COLOR, tickfont=dict(color=FONT_COLOR, size=10)),
                bar=dict(color=GOLD, thickness=0.25),
                bgcolor="#1E293B",
                bordercolor="rgba(0,0,0,0)",
                steps=[
                    dict(range=[0, 45], color="rgba(239,68,68,0.15)"),
                    dict(range=[45, 70], color="rgba(245,158,11,0.12)"),
                    dict(range=[70, 100], color="rgba(34,197,94,0.12)"),
                ],
                threshold=dict(line=dict(color=nivel_color, width=3), thickness=0.8, value=prediction),
            )
        ))
        fig_gauge.update_layout(
            paper_bgcolor=DARK_BG,
            font=dict(family="DM Sans", color=FONT_COLOR),
            margin=dict(l=20, r=20, t=20, b=20),
            height=280,
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.write("### 🧮 Ecuación de Regresión")
    if lp["modelo"] == "Completo" and c and len(c) >= 5:
        st.latex(
            fr"Rendimiento = {i:.2f} "
            fr"+ ({c[0]:.2f} \cdot Horas) "
            fr"+ ({c[1]:.2f} \cdot Puntaje) "
            fr"+ ({c[2]:.2f} \cdot Extra) "
            fr"+ ({c[3]:.2f} \cdot Sue\tilde{{n}}o) "
            fr"+ ({c[4]:.2f} \cdot Ex\acute{{a}}menes)"
        )
    elif lp["modelo"] == "Básico" and c and len(c) >= 2:
        st.latex(
            fr"Rendimiento = {i:.2f} "
            fr"+ ({c[0]:.2f} \cdot Horas) "
            fr"+ ({c[1]:.2f} \cdot Puntaje)"
        )
    else:
        st.info("No se pudo construir la ecuación (coeficientes no disponibles).")

else:
    if lottie_robot:
        st_lottie(lottie_robot, height=560, key="robot_inicio")


# ─────────────────────────────────────────────────────────────
# HISTORIAL
# ─────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("<br>", unsafe_allow_html=True)
    col_titulo, col_clear = st.columns([5, 1])

    with col_titulo:
        st.markdown("### 🕓 Historial de predicciones")

    with col_clear:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_prediction = None
            st.rerun()

    for h in st.session_state.history:
        color_h = "#22C55E" if h["score"] >= 70 else ("#F59E0B" if h["score"] >= 45 else "#EF4444")
        badge_h = "✦ Completo" if h["modelo"] == "Completo" else "◈ Básico"

        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
            background:rgba(30,41,59,0.7);border:1px solid rgba(245,158,11,0.2);
            border-radius:12px;padding:12px 18px;margin-bottom:8px;">
            <div style="display:flex;align-items:center;gap:14px">
                <div style="background:{color_h}22;color:{color_h};border-radius:10px;
                    padding:4px 14px;font-family:'DM Mono',monospace;font-weight:800;font-size:1.1rem;">
                    {h['score']}</div>
                <div>
                    <div style="color:#E2E8F0;font-size:0.85rem;font-weight:800">Rendimiento {h['nivel']}</div>
                    <div style="color:#94A3B8;font-size:0.72rem;margin-top:2px">
                        {badge_h} · {h['horas']}h estudio · Prev: {h['prev']}</div>
                </div>
            </div>
            <div style="color:#475569;font-size:0.72rem">{h['time']}</div>
        </div>
        """, unsafe_allow_html=True)