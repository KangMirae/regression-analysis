# 🎓 Academic Performance Prediction  
### *Student Performance Regression Project*

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**[🚀 Live Demo: Try here](https://regression-analysis.streamlit.app/)**

Machine Learning application that predicts student performance based on academic and behavioral factors.

</div>

---

## 📌 Project Overview
This project applies **Linear Regression** to predict students’ academic performance. Beyond just prediction, this tool serves as a simulator to visualize the impact of study habits on final grades.

---

## 🧠 The Two Final Models

### 🔵 Multivariable Model — *Full Version*
**"Maximum precision using all statistically significant variables."**

| Metric | Value |
|--------|-------|
| **R² Score** | **0.98** |
| **MAE (Mean Absolute Error)** | **±1.61 pts** |
| Input Variables | 5 Variables (Hours, Previous Score, Sleep, etc.) |

---

### 🟢 Two-Variable Model — *Basic Version*
**"Fast and interpretable prediction based on key factors."**

| Metric | Value |
|--------|-------|
| **R² Score** | **0.98** |
| **MAE (Mean Absolute Error)** | **±1.88 pts** |
| Input Variables | `Hours Studied` + `Previous Scores` |

---

## 📊 Key Findings
- **Previous Scores** showed the highest correlation with final performance (**0.92**).
- **Hours Studied** was the most actionable variable. Each additional hour of study increased predicted performance by approximately **2.85 points**.

---

## 🖥️ Application Interface
The app features a custom dark theme (navy + gold) with real-time simulation logic.

<div align="center">
  <img src="./assets/image.png" width="48%" />
  &nbsp;&nbsp;
  <img src="./assets/image1.png" width="48%" />
</div>

---

## 🛠️ Technologies Used
- **Engine:** Python, Scikit-Learn, Pandas, NumPy.
- **UI:** Streamlit, Plotly, Lottie.

---

## 🚀 Installation & Usage
1. **Clone:** `git clone https://github.com/KangMirae/regression-analysis.git`
2. **Install:** `uv sync`
3. **Run:** `uv run streamlit run app.py`

---

## 🤝 Collaboration
Developed with the amazing support of: [Ingrid](https://github.com/IngridMartinezB), [Gema](https://github.com/gemayc), and [Jonathan](https://github.com/JonnyBP).