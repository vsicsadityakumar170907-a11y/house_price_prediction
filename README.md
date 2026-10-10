# Kanpur House Price Prediction

An end-to-end machine learning project that estimates residential property prices across selected areas of Kanpur. It covers dataset exploration, train/test splitting, feature engineering, model training, evaluation, and interactive prediction using Python.

> **Project status:** Educational portfolio project. The included dataset is synthetic and does not represent verified listings, registered transactions, or current market prices. Predictions and evaluation scores must not be used for real estate decisions.

## What this project demonstrates

- A complete regression workflow, from raw CSV data to a saved prediction model
- Data exploration and a reproducible 80/20 train/test split
- Numeric and categorical feature preparation, including area/locality interactions
- A linear regression model implemented with Python's standard library
- Holdout evaluation with MAE, RMSE, and R²
- Command-line and local web-app entry points

## Model results

The current model was evaluated on 100 held-out rows from the synthetic dataset:

| Metric | Result |
| --- | ---: |
| Mean Absolute Error (MAE) | ₹394,882 |
| Root Mean Squared Error (RMSE) | ₹595,455 |
| R² | 0.962 |

These scores describe performance on this generated dataset only. They are not evidence of accuracy on real Kanpur property prices.

## Dataset

`data/kanpur_house_prices.csv` contains 500 synthetic records for these localities: Barra, Civil Lines, Govind Nagar, Kakadeo, Kalyanpur, Kidwai Nagar, Naubasta, Rawatpur, Shyam Nagar, and Swaroop Nagar.

Features include locality, property type, bedrooms, bathrooms, built-up and plot area, property age, floor information, parking, and furnishing. The target column is `price_inr`.

## Requirements

- Python 3.13 (the version used during development)
- No third-party Python packages are required by the core scripts.

Run commands from the repository root in PowerShell:

```powershell
python --version
python .\01_explore_data.py
python .\02_split_data.py
python .\03_prepare_features.py
python .\04_train_model.py
python .\07_evaluate_predictions.py
python .\06_interactive_predict.py
```

Run the data preparation and training steps in order before prediction. Training creates or refreshes `model.json`; evaluation writes `data/test_predictions.csv`.

### Optional local web interface

The repository also includes `08_web_app.py`. To launch it, run:

```powershell
python .\08_web_app.py
```

Then open the local address printed in the terminal. The web interface requires a trained `model.json`.

## Repository structure

```text
.
├── data/
│   └── kanpur_house_prices.csv
├── 01_explore_data.py
├── 02_split_data.py
├── 03_prepare_features.py
├── 04_train_model.py
├── 05_predict.py
├── 06_interactive_predict.py
├── 07_evaluate_predictions.py
├── 08_web_app.py
├── model.json
└── README.md
```

## Limitations and next steps

The dataset is synthetic, locality coverage is limited, and the model has not been validated against real transaction data. A practical next version should use reliable, legally obtained property data; document its source and collection date; compare against a simple baseline and other regression models; and evaluate with cross-validation and location-aware error analysis.

## Author

**Aditya Kumar**
Email- vsics.adityakumar170907@gmail.com
