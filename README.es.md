# 🎓 Predicción de Rendimiento Académico  
### *Proyecto de Regresión de Desempeño Estudiantil*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**[🚀 Demo en vivo: Pruébalo aquí](https://regression-analysis.streamlit.app/)**

Aplicación de Machine Learning que predice el rendimiento estudiantil basada en factores académicos y conductuales.

</div>

---

## 📌 Descripción del Proyecto
Este proyecto aplica **Regresión Lineal** para predecir el rendimiento académico de los estudiantes. Más allá de la simple predicción, esta herramienta funciona como un simulador interactivo para visualizar el impacto real de los hábitos de estudio en las calificaciones finales.

---

## 🧠 Los Dos Modelos Finales

### 🔵 Modelo Multivariable — *Versión Completa*
**"Máxima precisión utilizando todas las variables estadísticamente significativas."**

| Métrica | Valor |
|--------|-------|
| **R² Score** | **0.98** |
| **MAE (Error Absoluto Medio)** | **±1.61 pts** |
| Variables de entrada | 5 Variables (Horas, Notas previas, Sueño, etc.) |

---

### 🟢 Modelo de Dos Variables — *Versión Básica*
**"Predicción rápida e interpretable basada en factores clave."**

| Métrica | Valor |
|--------|-------|
| **R² Score** | **0.98** |
| **MAE (Error Absoluto Medio)** | **±1.88 pts** |
| Variables de entrada | `Horas de estudio` + `Notas anteriores` |

---

## 📊 Hallazgos Principales
- **Notas Anteriores:** Mostraron la correlación más alta con el rendimiento final (**0.92**).
- **Horas de Estudio:** Fue la variable más "accionable". Cada hora adicional de estudio incrementa el rendimiento predicho en aproximadamente **2.85 puntos**.

---

## 🖥️ Interfaz de la Aplicación
La app presenta un tema oscuro personalizado (*navy + gold*) con lógica de simulación en tiempo real.

<div align="center">
  <img src="./assets/image.png" width="48%" />
  &nbsp;&nbsp;
  <img src="./assets/image1.png" width="48%" />
</div>

---

## 🛠️ Tecnologías Utilizadas
- **Núcleo:** Python, Scikit-Learn, Pandas, NumPy.
- **Interfaz:** Streamlit, Plotly, Lottie.

---

## 🚀 Instalación y Uso
1. **Clonar:** `git clone https://github.com/KangMirae/regression-analysis.git`
2. **Instalar:** `uv sync`
3. **Ejecutar:** `uv run streamlit run app.py`

---

## 🤝 Colaboración
Desarrollado con el increíble apoyo de: [Ingrid](https://github.com/IngridMartinezB), [Gema](https://github.com/gemayc), y [Jonathan](https://github.com/JonnyBP).