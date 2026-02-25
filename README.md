🇪🇸 Spanish version available here: [README.es.md](README.es.md)

# 🎓 Academic Performance Prediction  
### *Student Performance Regression Project*


<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Machine Learning application that predicts student performance based on academic and behavioral factors.

</div>

---

## 📌 Project Overview

This project applies **supervised regression techniques** to predict students’ academic performance using study habits and historical academic data.

The objective is twofold:

- Identify the most influential variables affecting student success.
- Deliver an interactive and functional predictive tool built with Streamlit.

The dataset used is the well-known **Student Performance Dataset**, which includes variables such as study hours, sleep habits, extracurricular activities, and previous scores.

---

## 🤝 Team Methodology

The project followed a **collaborative and parallel workflow**, structured into three main phases:

### 1️⃣ Exploratory Data Analysis (EDA) — Individual

Each team member conducted independent EDA to:

- Analyze dataset structure and quality.
- Detect outliers and unusual distributions.
- Form individual hypotheses regarding variable relationships.

This approach minimized analytical bias and encouraged diverse perspectives.

---

### 2️⃣ Model Development — Individual

Each member independently developed regression models, experimenting with:

- Different combinations of predictor variables.
- Algorithms such as Linear Regression, Ridge, and Lasso.
- Hyperparameter tuning and cross-validation.

---

### 3️⃣ Final Model Selection — Collaborative

After comparing results, the team selected the two most robust approaches to integrate into the final application.

---

## 🧠 The Two Final Models

### 🔵 Multivariable Model — *Full Version* (`modelo_multiple.pkl`)

**"Maximum precision using all statistically significant variables."**

This model includes five impactful variables:

| Metric | Value |
|--------|-------|
| R² Score | **0.98** |
| Input Variables | `Hours Studied`, `Previous Scores`, `Extracurricular Activities`, `Sleep Hours`, `Sample Question Papers Practiced` |
| Ideal Use Case | Detailed and comprehensive student evaluation |

**Why does it perform well?**  
By combining historical academic performance with behavioral and lifestyle variables, the model captures a more complete representation of academic outcomes.

---

### 🟢 Two-Variable Model — *Basic Version* (`modelo_notas.pkl`)

**"Fast and interpretable prediction based on key factors."**

Built using only:

- 📚 `Hours Studied`
- 📊 `Previous Scores`

| Metric | Description |
|--------|------------|
| Input Variables | `Hours Studied` + `Previous Scores` |
| Strength | Simplicity and interpretability |
| Ideal Use Case | Quick assessment with limited available data |

These two variables represent the strongest combination between past performance and current effort.

---

## 📊 Key Findings

- **Previous Scores** showed the highest correlation with final performance (**0.92**), indicating strong academic consistency over time.
- **Hours Studied** was the most actionable variable. Each additional hour of study increased predicted performance by approximately **2.85 points**.
- **Sleep Hours** was included in the full model as a supporting behavioral factor.

---

## 🖥️ Application Interface

The app is built with **Streamlit** and features a custom dark theme (navy + gold), modern typography, and glassmorphism UI elements.

<div align="center">
  <img src="./assets/image.png" width="48%" />
  &nbsp;&nbsp;
  <img src="./assets/image1.png" width="48%" />
</div>

---

### Sidebar — Control Panel

The sidebar allows users to:

- Select between the Full and Basic models.
- Enter student input variables.
- Generate real-time predictions.
- Save predictions locally.
- View prediction history.

Input fields dynamically adjust depending on the selected model.

---

### Main Area — Prediction Output

Once a prediction is generated, the interface displays:

- 🎯 Predicted Performance Index
- 📊 Quick summary metrics
- 📉 Feature importance chart (Plotly)
- 🔵 Gauge visualization indicating performance level

Performance levels:

| Range | Level |
|-------|-------|
| 70 – 100 | High |
| 45 – 69 | Medium |
| 0 – 44 | Low |

---

## 🎨 Design

Custom CSS is injected into Streamlit using `st.markdown(..., unsafe_allow_html=True)`.

Design elements include:

- Dark navy background
- Gold accent highlights
- Glassmorphism containers
- Custom scrollbar styling
- Interactive hover effects

---

## 🛠️ Technologies Used

| Category | Tools |
|----------|-------|
| Language | Python 3.12 |
| Machine Learning | Scikit-Learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| UI Deployment | Streamlit |
| Model Serialization | Joblib (.pkl) |
| Dependency Management | uv / pip |

---

## 🚀 Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/Bootcamp-IA-P6/Proyecto5_Regression_Equipo1.git
cd proyecto5_regression_equipo1
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the application

```bash
uv run streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📁 Project Structure

```
Proyecto5_Regression_Equipo1/
│
├── 📂 .streamlit/
│   └── config.toml
│
├── 📂 assets/
│   ├── niu.json
│   ├── history.json
│
├── 📂 data/
│   └── Student_Performance.csv
│
├── 📂 notebooks/
│   ├── 01_eda_student_g.ipynb
│   ├── 02_entrenamiento_modelo_g.ipynb
│   ├── horas_estudio_sueno_I.ipynb
│   ├── student_perfomance_regression_j.ipynb
│   ├── student_perfomance_regression_m.ipynb
│   ├── modelo_multiple.pkl
│   └── modelo_notas.pkl
│
├── 📂 reports/
│   └── EDA_REPORT.md
│
├── app.py
├── pyproject.toml
└── README.md
```

---

## 🤝 Collaboration

This project was developed collaboratively as part of a Machine Learning training program.

Collaborated with:

- [Ingrid](https://github.com/IngridMartinezB)
- [Gema](https://github.com/gemayc)
- [Jonathan](https://github.com/JonnyBP)
