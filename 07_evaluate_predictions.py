import csv
import json

with open("model.json", encoding="utf-8") as file:
    model = json.load(file)

with open("data/test_ready.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    headers = next(reader)
    rows = [[float(value) for value in row] for row in reader]

if headers[:-1] != model["feature_names"]:
    raise ValueError("Test file ke features model se match nahi karte. Pehle 03 aur 04 run karein.")

results = []

for index, row in enumerate(rows, start=1):
    features = row[:-1]
    actual_inr = row[-1]

    scaled = [
        (value - mean) / std
        for value, mean, std in zip(features, model["means"], model["stds"])
    ]

    predicted_lakh = (
        model["bias"]
        + sum(weight * value for weight, value in zip(model["weights"], scaled))
    ) * model["target_std_lakh"] + model["target_mean_lakh"]

    predicted_inr = predicted_lakh * 100_000
    error_inr = abs(predicted_inr - actual_inr)
    error_percent = error_inr / actual_inr * 100 if actual_inr else 0

    results.append([
        index,
        round(actual_inr),
        round(predicted_inr),
        round(error_inr),
        round(error_percent, 2),
    ])

with open("data/test_predictions.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "test_row",
        "actual_price_inr",
        "predicted_price_inr",
        "absolute_error_inr",
        "error_percent",
    ])
    writer.writerows(results)

print("Comparison saved: data/test_predictions.csv")
print("\nSabse zyada error wale 5 test records:")
for result in sorted(results, key=lambda item: item[3], reverse=True)[:5]:
    print(result)