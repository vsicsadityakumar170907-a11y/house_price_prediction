# Kanpur House Price Prediction

**Author:** Aditya Kumar

Python standard library se banaya gaya house-price prediction practice project.

## Dataset

Dataset mein Kanpur ke localities ke 500 synthetic property records hain. `price_inr` prediction ka target column hai.

**Important:** Data aur predictions learning ke liye hain. Yeh actual sale prices ya real property valuations nahi hain.

## Project chalana

Commands project ke main folder se chalayein:

1. Data inspect karein: `python .\01_explore_data.py`
2. Training aur testing data banayein: `python .\02_split_data.py`
3. Features prepare karein: `python .\03_prepare_features.py`
4. Model train karein: `python .\04_train_model.py`
5. Test predictions evaluate karein: `python .\07_evaluate_predictions.py`
6. Terminal se prediction karein: `python .\06_interactive_predict.py`
7. Browser app chalayein: `python .\08_web_app.py`

Browser app chalne ke baad `http://127.0.0.1:8000` kholein. Server rokne ke liye terminal mein `Ctrl+C` dabayein.

Model `model.json` file mein save hota hai. Data dobara prepare karne par model ko phir se train karein.

## Model evaluation

Current synthetic test set par:

- MAE: ₹394,882
- RMSE: ₹595,455
- R²: 0.962

Yeh scores sirf synthetic practice data par model ke results hain; real Kanpur market accuracy nahi dikhate.