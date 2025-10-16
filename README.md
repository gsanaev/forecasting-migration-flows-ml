# 🌍 Forecasting Migration Flows with Machine Learning 🚀

> A reproducible data science pipeline to forecast international migration flows (1990–2023, extended to 2030) using demographic, economic, and human development indicators.  
> Built with **Linear Regression** and **Random Forest** models, and interpreted using **SHAP** explainability methods.

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-completed-success)

---

## 📘 View Results Online

You can explore the full analysis directly here:

- <a href="https://gsanaev.github.io/forecasting-migration-flows-ml/01-data-preparation-cleaning.html" target="_blank">🧹 Data Preparation & Cleaning</a>  
- <a href="https://gsanaev.github.io/forecasting-migration-flows-ml/02-exploratory-data-analysis.html" target="_blank">🔍 Exploratory Data Analysis (EDA)</a>  
- <a href="https://gsanaev.github.io/forecasting-migration-flows-ml/03-feature-engineering-modeling.html" target="_blank">⚙️ Feature Engineering & Modeling</a>  
- <a href="https://gsanaev.github.io/forecasting-migration-flows-ml/04-model-interpretation-scenario-analysis.html" target="_blank">🌳 Model Interpretation & Scenario Analysis</a>  
- <a href="https://gsanaev.github.io/forecasting-migration-flows-ml/05-forecasting-validation.html" target="_blank">📈 Forecasting & Validation</a>  

---

## 📊 Project Overview

**Problem Statement:**  
International migration is driven by intertwined economic, demographic, and social dynamics. Understanding these drivers and projecting future migration trends are essential for policy and planning.

**Goal:**  
To build a **reproducible forecasting pipeline** that models **net migration (per 1,000 people)** for 168 countries (1990–2023) using open data from the **World Bank** and **UNDP**, and extends forecasts through **2030** under multiple socioeconomic scenarios.

**Methods:**  
- Automated data extraction from **World Bank WDI API**  
- Manual integration of **UNDP Human Development Index (HDI)**  
- **Feature engineering** (lags, caps, interactions, scaling)  
- **Machine learning** (Linear Regression, Random Forest)  
- **Explainability** with SHAP values  
- **Forecasting with scenario-based inference and uncertainty intervals**  

---

## 🎯 Key Insights

- 📈 **Economic and demographic factors** (GDP growth, unemployment, fertility) dominate migration variability.  
- 🔍 **HDI and population growth** contribute significantly to explaining migration intensity.  
- 🌍 **Regional heterogeneity**: Income groups and regional aggregates show distinct migration patterns.  
- 💡 **Forecast performance** is stable with strong temporal generalization (1990–2023).  
- 📅 **Forecasting update:** The pipeline now extends migration projections through **2030**, generating **baseline, high-growth, crisis, and demographic-pressure** scenarios with **90 % prediction intervals** and global/regional aggregation outputs.  

---

## 📁 Repository Structure

```
├── data/
│   ├── raw/                         # Original World Bank & UNDP data
│   │   ├── hdr-data.xlsx            # Manual UNDP HDI data
│   │   ├── wdi_data.csv             # Extracted via src/migration/wdi_data.py
│   │   ├── wdi_metadata.csv         # WDI metadata
│   └── processed/                   # Cleaned and transformed datasets
│       ├── countries_clean.csv          # Country-level cleaned dataset
│       ├── aggregates_clean.csv         # Regional/income group aggregates
│       ├── countries_only.csv           # Filtered country subset (no aggregates)
│       ├── aggregates_only.csv          # Filtered aggregates subset
│       ├── dropped_countries.csv        # Countries removed due to missingness
│       ├── model_ready.csv              # Final dataset for ML training
│       ├── model_ready.parquet          # Optimized parquet version
│       ├── wdi_hdr.csv                  # Combined WDI + HDI merged dataset
│       └── .gitkeep
│
├── data_reserve/                    # Backup merged dataset
│   └── wdi_hdr_2025-10-13.csv
│
├── src/migration/
│   ├── wdi_data.py                  # Downloads WDI indicators
│   ├── merge_data.py                # Merges WDI & HDI data
│   └── __init__.py
│
├── notebooks/
│   ├── 01-data-preparation-cleaning.ipynb
│   ├── 02-exploratory-data-analysis.ipynb
│   ├── 03-feature-engineering-modeling.ipynb
│   ├── 04-model-interpretation-scenario-analysis.ipynb
│   └── 05-forecasting-validation.ipynb
│
├── models/                          # Trained models & artifacts
│   ├── random_forest_model.pkl          # Final trained Random Forest model
│   ├── X_columns.pkl                    # Feature column order used in training
│   ├── 03_rf_feature_importance.csv     # SHAP / permutation feature importance
│   ├── 03_results_summary.csv           # Cross-validation and training metrics
│   └── .gitkeep
│
├── outputs/                         # Evaluation and forecasting results
│   ├── backtest_metrics_by_fold.csv         # Fold-level performance metrics
│   ├── backtest_diagnostics_by_income.csv   # Metrics aggregated by income group
│   ├── backtest_oof_predictions.csv         # Out-of-fold predictions
│   ├── forecast_results_2024_2030.csv       # Clean future forecasts (2024–2030)
│   ├── forecast_global_trends.csv           # Global scenario mean trends
│   ├── residuals_vs_pred.png                # Residual plot visualization
│   └── .gitkeep
│
├── docs/                            # Executed HTML notebooks and figures
│   ├── 01-data-preparation-cleaning.html
│   ├── 02-exploratory-data-analysis.html
│   ├── 03-feature-engineering-modeling.html
│   ├── 04-model-interpretation-scenario-analysis.html
│   ├── 05-forecasting-validation.html
│   └── correlation_heatmap_country_level.png
│
├── DATA_INSTRUCTIONS.md             # How to download UNDP HDI data
├── README.md                        # Project documentation
└── pyproject.toml                   # uv project configuration
```

---

## 🔧 Technologies Used

**Programming language:**  
- Python 3.12

**Core libraries:**  
- `pandas`, `numpy`, `matplotlib`, `seaborn`  
- `scikit-learn`, `shap`, `joblib`  
- `pathlib`, `tqdm`, `warnings`  

**Tools:**  
- JupyterLab  
- uv (for dependency and environment management)  
- Git & GitHub  

---

## 📊 Data

**Sources:**  
- 🌐 **World Bank – World Development Indicators (WDI)**  
  - Downloaded automatically via:
    ```bash
    uv run python -m src.migration.wdi_data
    ```
  - Produces `wdi_data.csv` and `wdi_metadata.csv` in `data/raw/`

- 🧭 **UNDP – Human Development Index (HDI)**  
  - Download manually from [UNDP Data Center](https://hdr.undp.org/data-center/documentation-and-downloads)  
  - Save as `hdr-data.xlsx` in `data/raw/`  
  - See detailed guide: [`DATA_INSTRUCTIONS.md`](./DATA_INSTRUCTIONS.md)

- 🔗 **Merged Dataset (HDI + WDI)**  
  - Created using:
    ```bash
    uv run python -m src.migration.merge_data
    ```
  - Output: `data/processed/wdi_hdr.csv`

- 🗃️ **Backup (for reproducibility)**  
  - A reference copy is stored as `data_reserve/wdi_hdr_2025-10-13.csv`

---

## 🤖 Methodology

### Data Preparation
- Cleans and merges WDI and HDI datasets  
- Removes aggregates and incomplete countries  
- Converts net migration to **per 1,000 people**

### Exploratory Data Analysis (EDA)
- Examines indicator distributions and missingness  
- Visualizes migration trends (global, regional, income-group)  
- Produces correlation heatmaps and outlier diagnostics  

### Feature Engineering & Modeling
- Constructs **target and feature matrices**  
- Applies **lags, interactions**, and scaling  
- Implements **time-aware validation splits**

### Model Interpretation & Scenario Analysis
- Trains and interprets **Random Forest** using **SHAP values**  
- Runs **economic and demographic what-if scenarios**

### Forecasting & Validation
- Extends migration forecasts through **2030**  
- Uses **expanding-window and rolling-origin** temporal validation  
- Estimates **90 % empirical prediction intervals** from residuals  
- Generates **baseline, growth, crisis, and demographic pressure** scenarios  
- Exports clean global and regional forecast artifacts  

---

## 📈 Results Summary

| Metric | Cross-Validation |
|--------|------------------|
| **MAE** | ~3.0–3.5 |
| **RMSE** | ~5.5–6.5 |
| **R²** | 0.60–0.65 |
| **90 % PI coverage** | ≈ 0.75 |

**Interpretation:**  
The Random Forest model demonstrates stable temporal performance and solid explanatory power.  
Results indicate consistent accuracy across income groups, with best performance among high-income economies.

**Top predictive drivers:**  
GDP growth, unemployment, population growth, HDI, and fertility rate.

**Most variable regions:**  
Sub-Saharan Africa, Middle East & North Africa, and Europe & Central Asia.

**Forecasting results (2024–2030):**  
Baseline forecasts show stable global migration inflows, while high-growth and crisis scenarios diverge moderately, reflecting macroeconomic sensitivity and demographic pressures.

---

## 🚀 Reproducibility

### Setup
```bash
# Clone repository
git clone https://github.com/gsanaev/forecasting-migration-flows-ml.git
cd forecasting-migration-flows-ml

# Sync environment (installs Python and dependencies)
uv sync
```

### Execution
Ensure raw data is available in `data/raw/`, then run:

```bash
# 1. Retrieve World Bank data
uv run python -m src.migration.wdi_data

# 2. Merge with HDI dataset
uv run python -m src.migration.merge_data
```

Finally, execute notebooks in sequence:

```bash
# 1. notebooks/01-data-preparation-cleaning.ipynb
# 2. notebooks/02-exploratory-data-analysis.ipynb
# 3. notebooks/03-feature-engineering-modeling.ipynb
# 4. notebooks/04-model-interpretation-scenario-analysis.ipynb
# 5. notebooks/05-forecasting-validation.ipynb
```

---

## 🎓 About This Project

**Context:**  
Independent research on global migration forecasting using open data and interpretable machine learning.

**Period:**  
2025  

**Author:**  
Golib Sanaev  

---

## 📞 Contact

**GitHub:** [@gsanaev](https://github.com/gsanaev)  
**Email:** gsanaev@gmail.com  
**LinkedIn:** [golib-sanaev](https://linkedin.com/in/golib-sanaev)

---

## 🙏 Acknowledgements
- [StackFuel](https://stackfuel.com/) — for supporting applied ML learning  
- [World Bank](https://data.worldbank.org/) and [UNDP](https://hdr.undp.org/) — for open datasets  
- `scikit-learn`, `SHAP`, and `pandas` communities — for transparent ML tools  

---

⭐ **If you find this project insightful, please give it a star!**
