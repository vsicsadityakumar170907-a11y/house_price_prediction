import json

with open("model.json", encoding="utf-8") as file:
    model = json.load(file)


def ask_number(prompt):
    while True:
        try:
            return float(input(prompt + ": "))
        except ValueError:
            print("Kripya number enter karein.")


def choose(prompt, options):
    print("\n" + prompt)

    for number, option in enumerate(options, start=1):
        print(f"{number}. {option}")

    while True:
        try:
            choice = int(input("Number chunein: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass

        print("List mein se valid number chunein.")


house = {
    "bedrooms": ask_number("Bedrooms"),
    "bathrooms": ask_number("Bathrooms"),
    "builtup_area_sqft": ask_number("Built-up area (sq ft)"),
    "plot_area_sqft": ask_number("Plot area (sq ft)"),
    "property_age_years": ask_number("Property age (years)"),
    "floor_number": ask_number("Floor number"),
    "total_floors": ask_number("Building mein total floors"),
    "locality": choose("Locality:", [
        "Barra",
        "Civil Lines",
        "Govind Nagar",
        "Kakadeo",
        "Kalyanpur",
        "Kidwai Nagar",
        "Naubasta",
        "Rawatpur",
        "Shyam Nagar",
        "Swaroop Nagar",
    ]),
    "property_type": choose("Property type:", [
        "Apartment",
        "Independent House",
    ]),
    "parking": choose("Parking:", ["Yes", "No"]),
    "furnishing": choose("Furnishing:", [
        "Furnished",
        "Semi-furnished",
        "Unfurnished",
    ]),
}


# Input validation
issues = []

if not 1 <= house["bedrooms"] <= 4:
    issues.append("Bedrooms 1 se 4 ke beech hone chahiye.")

if not 1 <= house["bathrooms"] <= house["bedrooms"]:
    issues.append("Bathrooms 1 se bedrooms tak hone chahiye.")

if not 300 <= house["builtup_area_sqft"] <= 1900:
    issues.append("Built-up area 300–1900 sq ft ke beech honi chahiye.")

if not 0 <= house["property_age_years"] <= 35:
    issues.append("Property age 0–35 years ke beech honi chahiye.")

builtup = house["builtup_area_sqft"]
plot_area = house["plot_area_sqft"]
ratio = plot_area / builtup if builtup > 0 else 0

if house["property_type"] == "Apartment":
    floors_ok = 3 <= house["total_floors"] <= 12
    area_ok = builtup > 0 and 0.90 <= ratio <= 1.12
else:
    floors_ok = 1 <= house["total_floors"] <= 3
    area_ok = builtup > 0 and 0.85 <= ratio <= 1.60

if not floors_ok:
    issues.append(
        "Is property type ke floors training data ki range se bahar hain."
    )

if not 0 <= house["floor_number"] < house["total_floors"]:
    issues.append("Floor number total floors se kam hona chahiye.")

if not area_ok:
    issues.append(
        "Plot aur built-up area ka ratio training data ki range se bahar hai."
    )

if issues:
    print("\nInput check nahi hua:")
    for issue in issues:
        print("-", issue)
    raise SystemExit


# Naye interaction features wala model hona zaroori hai
has_interactions = any(
    name.startswith("builtup_x_locality_")
    for name in model["feature_names"]
)

if not has_interactions:
    print(
        "\nmodel.json purane features wala lagta hai. "
        "Pehle 03_prepare_features.py aur 04_train_model.py chalayein."
    )
    raise SystemExit


# Model ke feature order mein input features banana
features = []

for name in model["feature_names"]:
    value = 0.0

    if name in house:
        value = float(house[name])

    elif name.startswith("builtup_x_locality_"):
        locality = name[len("builtup_x_locality_"):]
        value = house["builtup_area_sqft"] * (
            house["locality"] == locality
        )

    elif name.startswith("plot_x_locality_"):
        locality = name[len("plot_x_locality_"):]
        value = house["plot_area_sqft"] * (
            house["locality"] == locality
        )

    elif name == "builtup_x_property_type_Independent House":
        value = house["builtup_area_sqft"] * (
            house["property_type"] == "Independent House"
        )

    else:
        for category in [
            "locality",
            "property_type",
            "parking",
            "furnishing",
        ]:
            prefix = category + "_"

            if name.startswith(prefix):
                category_value = name[len(prefix):]
                value = 1.0 if house[category] == category_value else 0.0
                break

    features.append(float(value))


# Features ko training ke mean aur standard deviation se scale karna
if not (
    len(features)
    == len(model["means"])
    == len(model["stds"])
    == len(model["weights"])
):
    raise ValueError(
        "Model ke feature sizes match nahi karte. "
        "03_prepare_features.py aur 04_train_model.py dobara chalayein."
    )

scaled = [
    (value - mean) / std
    for value, mean, std in zip(features, model["means"], model["stds"])
]

price_lakh = (
    model["bias"]
    + sum(
        weight * value
        for weight, value in zip(model["weights"], scaled)
    )
) * model["target_std_lakh"] + model["target_mean_lakh"]

if price_lakh < 0:
    print("\nModel ne negative estimate diya; is input par result valid nahi hai.")
else:
    print(f"\nEstimated practice price: ₹{price_lakh * 100_000:,.0f}")