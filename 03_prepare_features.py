import csv

numeric_columns = [
    "bedrooms",
    "bathrooms",
    "builtup_area_sqft",
    "plot_area_sqft",
    "property_age_years",
    "floor_number",
    "total_floors",
]

categorical_columns = [
    "locality",
    "property_type",
    "parking",
    "furnishing",
]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


train = read_csv("data/train.csv")
test = read_csv("data/test.csv")

# Categories sirf training data se seekhenge
categories = {
    column: sorted({row[column] for row in train})
    for column in categorical_columns
}

feature_names = numeric_columns.copy()

# Categorical columns ko one-hot encode karna
# Har category ki pehli value baseline rahegi
for column in categorical_columns:
    feature_names += [
        f"{column}_{value}"
        for value in categories[column][1:]
    ]

# Locality ke hisaab se area ka price effect capture karne ke features
locality_values = categories["locality"][1:]

for locality in locality_values:
    feature_names.extend([
        f"builtup_x_locality_{locality}",
        f"plot_x_locality_{locality}",
    ])

# Independent House aur Apartment ke area effects alag capture karna
feature_names.append("builtup_x_property_type_Independent House")


def make_features(row):
    values = [float(row[column]) for column in numeric_columns]

    # Categorical one-hot features
    for column in categorical_columns:
        for value in categories[column][1:]:
            values.append(1.0 if row[column] == value else 0.0)

    builtup = float(row["builtup_area_sqft"])
    plot_area = float(row["plot_area_sqft"])

    # Built-up aur plot area ka locality-specific effect
    for locality in locality_values:
        is_locality = 1.0 if row["locality"] == locality else 0.0
        values.extend([
            builtup * is_locality,
            plot_area * is_locality,
        ])

    # Independent House ke built-up area ka effect
    is_independent_house = (
        1.0 if row["property_type"] == "Independent House" else 0.0
    )
    values.append(builtup * is_independent_house)

    return values


def save_ready_file(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(feature_names + ["price_inr"])

        for row in rows:
            writer.writerow(make_features(row) + [row["price_inr"]])


save_ready_file("data/train_ready.csv", train)
save_ready_file("data/test_ready.csv", test)

print("Features:", len(feature_names))
print("Training rows prepared:", len(train))
print("Testing rows prepared:", len(test))
print("Feature names:", feature_names)