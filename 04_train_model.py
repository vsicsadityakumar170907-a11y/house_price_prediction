import csv
import json
import math

def read_ready_file(path):
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = [[float(value) for value in row] for row in reader]

    feature_names = headers[:-1]
    X = [row[:-1] for row in rows]
    y = [row[-1] / 100_000 for row in rows]  # rupees ko lakh mein
    return feature_names, X, y

feature_names, X_train, y_train = read_ready_file("data/train_ready.csv")
test_names, X_test, y_test = read_ready_file("data/test_ready.csv")

# Features ko training data ke mean/std se scale karte hain
means = [sum(row[j] for row in X_train) / len(X_train)
         for j in range(len(feature_names))]

stds = []
for j in range(len(feature_names)):
    variance = sum((row[j] - means[j]) ** 2 for row in X_train) / len(X_train)
    stds.append(math.sqrt(variance) or 1.0)

def scale_features(X):
    return [
        [(row[j] - means[j]) / stds[j] for j in range(len(feature_names))]
        for row in X
    ]

X_train = scale_features(X_train)
X_test = scale_features(X_test)

# Target price ko bhi scale karte hain
y_mean = sum(y_train) / len(y_train)
y_std = math.sqrt(sum((value - y_mean) ** 2 for value in y_train) / len(y_train)) or 1.0
y_train_scaled = [(value - y_mean) / y_std for value in y_train]

# Gradient descent se model train
weights = [0.0] * len(feature_names)
bias = 0.0
learning_rate = 0.03
epochs = 2500

for _ in range(epochs):
    errors = [
        bias + sum(w * x for w, x in zip(weights, row)) - target
        for row, target in zip(X_train, y_train_scaled)
    ]

    bias -= learning_rate * sum(errors) / len(errors)

    for j in range(len(weights)):
        gradient = sum(error * row[j] for error, row in zip(errors, X_train))
        weights[j] -= learning_rate * gradient / len(errors)

# Test set par predictions
predictions_lakh = [
    (bias + sum(w * x for w, x in zip(weights, row))) * y_std + y_mean
    for row in X_test
]

actual_lakh = y_test
errors_inr = [(pred - actual) * 100_000
              for pred, actual in zip(predictions_lakh, actual_lakh)]

mae = sum(abs(error) for error in errors_inr) / len(errors_inr)
rmse = math.sqrt(sum(error ** 2 for error in errors_inr) / len(errors_inr))

actual_mean = sum(actual_lakh) / len(actual_lakh)
total_variation = sum((value - actual_mean) ** 2 for value in actual_lakh)
remaining_error = sum((pred - actual) ** 2
                      for pred, actual in zip(predictions_lakh, actual_lakh))
r2 = 1 - remaining_error / total_variation if total_variation else 0

print(f"Test records: {len(X_test)}")
print(f"MAE: ₹{mae:,.0f}")
print(f"RMSE: ₹{rmse:,.0f}")
print(f"R² score: {r2:.3f}")

# Trained model ko future prediction ke liye save karte hain
model = {
    "feature_names": feature_names,
    "means": means,
    "stds": stds,
    "weights": weights,
    "bias": bias,
    "target_mean_lakh": y_mean,
    "target_std_lakh": y_std,
}
with open("model.json", "w", encoding="utf-8") as file:
    json.dump(model, file, indent=2)

print("Model saved: model.json")