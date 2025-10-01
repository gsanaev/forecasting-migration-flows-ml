# Forecasting Migration Flows with Machine Learning

> This project explores the determinants of international migration using World Bank Indicators (1990–2023) and the Human Development Index (HDI) across 168 countries. By applying machine learning models, it aims to forecast net migration (per 1,000 people) and identify the key demographic, economic, and social drivers of global migration flows.

## 📊 Project overview

**Problem Statement:** 
International migration is influenced by complex demographic, economic, social, and technological factors. Understanding these drivers is critical for forecasting migration flows and informing policy decisions.

**Objective:** 
To forecast **net migration (per 1,000 people)** across 168 countries (1990–2023) and identify the most influential determinants of migration using demographic, economic, and human development indicators.

**Methods:** 
Exploratory data analysis, feature engineering, and machine learning models including **Linear Regression, Ridge Regression, Random Forest**, and **SHAP** for model interpretation.

## 🎯 Key Findings

- 📈 **Finding 1:** Kurze Beschreibung
- 🔍 **Finding 2:** Kurze Beschreibung  
- 💡 **Finding 3:** Kurze Beschreibung

## 📁 Repository Structure

```
├── data/
│   ├── raw/                    # Original World Bank & UNDP data
│   └── processed/              # Cleaned and transformed data
├── notebooks/                  # Jupyter Notebooks
│   └── 01_data_prep.ipynb      # Data preparation
│   └── 02_eda.ipynb            # Exploratory Data Analysis
│   └── 03_modeling.ipynb       # ML models (LR, Ridge, RF)
│   └── 04_results.ipynb        # Results & SHAP interpretation
├── src/dpp                     # Python Module
├── test/                       # Unit Tests
├── pyproject.toml              # Project configuration
└── docs/                       # Additional documentation
```

## 🔧 Technologies Used

**Programmiersprachen:**
Python

**Libraries & Frameworks:**
pandas, numpy, scikit-learn, matplotlib, seaborn, shap

**Tools:**
Jupyter, Git/GitHub

## 📊 Data

**Data Source::** 
- World Bank World Development Indicators
- UNDP Human Development Index 

**Dataset Size:**
- **Countries:** 168
- **Years:** 1990-2023 (34 years)
- **Observations:** 5,712

**Important Features:**
- **Demographics:** population, density, fertility, life expectancy, under-5 mortality, urbanization
- **Economics:** GDP per capita, GDP growth, exports, imports, unemployment
- **Technology:** mobile subscriptions
- **Human Development:** HDI
- **Target:** Net migration (per 1,000 people)

## 🤖 Methodology

### Data Preprocessing
- Cleaned missing values, harmonized country-year datasets
- Transformed net migration into **per 1,000 population**

### Modeling Approach  
- Baseline: Linear Regression
- Regularized models: Ridge Regression
- Nonlinear: Random Forest
- Interpretability: SHAP values

### Evaluation
- Performance metrics: RMSE, MAE, R²
- Feature importance and SHAP analysis

## 📈 Results
(to be filled in after analysis)

**Model Performance:**
<!-- Deine besten Metriken (Accuracy, RMSE, etc.) -->

**Key Visualizations:**
<!-- Verweis auf Key-Plots in deinen Notebooks -->

## 🚀 Reproducibility

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/migration-forecasting-ml.git
cd migration-forecasting-ml

# Install dependencies
uv sync
```

### Execution
```bash
# Run the notebooks in order:
# 1. notebooks/01_data_prep.ipynb
# 2. notebooks/02_eda.ipynb  
# 3. notebooks/03_modeling.ipynb
# 4. notebooks/04_results.ipynb
```

## 🎓 About this Project

**Context:** 
Independent research project on migration forecasting with machine learning.

**Timeframe:** 
2025

**Autor:** 
Golib Sanaev

## 📞 Contact

**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**E-Mail:** gsanaev@gmail.com  
**LinkedIn:** [golib-sanaev](https://linkedin.com/in/golib-sanaev/)

## 🙏 Acknowledgments
StackFuel Team
World Bank and UNDP for open data
scikit-learn & SHAP communities for ML tooling

**⭐ If you find this project interesting, please give it a star!**
