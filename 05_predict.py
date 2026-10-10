import json

with open("model.json", encoding="utf-8") as file:
    model = json.load(file)

# Sample ghar: values badal kar doosre ghar ki prediction try karein
house = {
    "bedrooms": 2,
    "bathrooms": 2,
    "builtup_area_sqft": 950,
    "plot_area_sqft": 950,
    "property_age_years": 5,
    "floor_number": 2,
    "total_floors": 8,
    "locality": "Kalyanpur",
    "property_type": "Apartment",
    "parking": "Yes",
    "furnishing": "Semi-furnished",
}

features = []

for name in model["feature_names"]:
    value = 0.0

    if name in house:
        value = float(house[name])
    else:
        for category in ["locality", "property_type", "parking", "furnishing"]:
            prefix = category + "_"
            if name.startswith(prefix) and house[category] == name[len(prefix):]:
                value = 1.0
                break

    features.append(value)

scaled_features = [
    (value - mean) / std
    for value, mean, std in zip(features, model["means"], model["stds"])
]

predicted_lakh = (
    model["bias"]
    + sum(weight * value
          for weight, value in zip(model["weights"], scaled_features))
) * model["target_std_lakh"] + model["target_mean_lakh"]

print(f"Predicted price: ₹{predicted_lakh * 100_000:,.0f}")