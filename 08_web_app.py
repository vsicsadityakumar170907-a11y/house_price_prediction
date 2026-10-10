import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


# Trained model load karein
with open("model.json", encoding="utf-8") as file:
    model = json.load(file)

# Check karein ki model naye interaction features ke saath train hua hai
if not any(
    name.startswith("builtup_x_locality_")
    for name in model["feature_names"]
):
    raise SystemExit(
        "Pehle 03_prepare_features.py aur 04_train_model.py chalakar "
        "naya model.json banayein."
    )


LOCALITIES = [
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
]


def options(values):
    html_options = []

    for index, value in enumerate(values):
        selected = " selected" if index == 0 else ""
        html_options.append(
            f'<option value="{value}"{selected}>{value}</option>'
        )

    return "".join(html_options)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kanpur HomePrice</title>

<style>
:root {
    --navy: #142b4a;
    --blue: #2864dc;
    --muted: #718096;
    --line: #e1e8f0;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    min-height: 100vh;
    font-family: "Segoe UI", Arial, sans-serif;
    color: var(--navy);
    background:
        radial-gradient(circle at 8% 8%, #dbeafe 0, transparent 30%),
        linear-gradient(135deg, #f5f8fd, #edf3fb);
}

.page {
    width: min(980px, calc(100% - 32px));
    margin: 42px auto;
}

.hero {
    padding: 12px 4px 24px;
}

.brand {
    display: inline-block;
    margin-bottom: 14px;
    padding: 8px 12px;
    color: #2455a7;
    background: #e4edff;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

h1 {
    margin: 0;
    font-size: clamp(30px, 5vw, 44px);
    letter-spacing: -1.5px;
}

.subtitle {
    max-width: 620px;
    margin: 10px 0 0;
    color: var(--muted);
    line-height: 1.6;
}

.card {
    padding: clamp(20px, 4vw, 34px);
    background: #fff;
    border: 1px solid #e9eef5;
    border-radius: 20px;
    box-shadow: 0 18px 50px #19365b12;
}

.card-heading {
    margin-bottom: 22px;
}

.card-heading h2 {
    margin: 0 0 6px;
    font-size: 21px;
}

.card-heading p {
    margin: 0;
    color: var(--muted);
    font-size: 14px;
}

form {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 18px;
}

label {
    display: grid;
    gap: 8px;
    color: #344760;
    font-size: 13px;
    font-weight: 600;
}

input,
select {
    width: 100%;
    min-height: 46px;
    padding: 10px 12px;
    color: var(--navy);
    background: #fbfcfe;
    border: 1px solid var(--line);
    border-radius: 10px;
    font: inherit;
    font-size: 15px;
}

input:focus,
select:focus {
    outline: 3px solid #2864dc22;
    border-color: var(--blue);
}

button {
    grid-column: 1 / -1;
    min-height: 50px;
    margin-top: 5px;
    color: white;
    background: linear-gradient(100deg, #2864dc, #1748b7);
    border: 0;
    border-radius: 11px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 8px 18px #2864dc30;
}

button:hover {
    filter: brightness(1.06);
    transform: translateY(-1px);
}

.result {
    margin-top: 22px;
    padding: 20px;
    color: #14532d;
    background: linear-gradient(120deg, #e9f9ef, #f4fcf6);
    border: 1px solid #c9efd5;
    border-radius: 12px;
    font-size: 21px;
    font-weight: 700;
}

.error {
    margin-top: 22px;
    padding: 18px;
    color: #8a2c20;
    background: #fff3f0;
    border: 1px solid #ffd5cc;
    border-radius: 12px;
}

.note {
    margin: 18px 2px 0;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.6;
}

@media (max-width: 620px) {
    .page {
        margin: 22px auto;
    }

    form {
        grid-template-columns: 1fr;
    }

    button {
        grid-column: 1;
    }
}
</style>
</head>

<body>
<main class="page">
    <header class="hero">
        <div class="brand">⌂ &nbsp; KANPUR • PROPERTY INSIGHTS</div>
        <h1>Find a home's estimated value</h1>
        <p class="subtitle">
            Property details enter karein aur apne practice model se
            ek estimated price dekhein.
        </p>
    </header>

    <section class="card">
        <div class="card-heading">
            <h2>Property details</h2>
            <p>Sabhi areas square feet mein enter karein.</p>
        </div>

        <form method="post">
            <label>Locality
                <select name="locality">LOCALITY_OPTIONS</select>
            </label>

            <label>Property type
                <select name="property_type">
                    <option>Apartment</option>
                    <option>Independent House</option>
                </select>
            </label>

            <label>Bedrooms
                <input name="bedrooms" type="number" min="1" max="4"
                       step="1" value="2" required>
            </label>

            <label>Bathrooms
                <input name="bathrooms" type="number" min="1" max="4"
                       step="1" value="2" required>
            </label>

            <label>Built-up area (sq ft)
                <input name="builtup_area_sqft" type="number"
                       min="300" max="1900" value="950" required>
            </label>

            <label>Plot area (sq ft)
                <input name="plot_area_sqft" type="number"
                       min="1" value="950" required>
            </label>

            <label>Property age (years)
                <input name="property_age_years" type="number"
                       min="0" max="35" value="5" required>
            </label>

            <label>Floor number
                <input name="floor_number" type="number"
                       min="0" max="11" value="1" required>
            </label>

            <label>Total floors
                <input name="total_floors" type="number"
                       min="1" max="12" value="8" required>
            </label>

            <label>Parking
                <select name="parking">
                    <option>Yes</option>
                    <option>No</option>
                </select>
            </label>

            <label>Furnishing
                <select name="furnishing">
                    <option>Furnished</option>
                    <option>Semi-furnished</option>
                    <option>Unfurnished</option>
                </select>
            </label>

            <button type="submit">Estimate price &nbsp; →</button>
        </form>

        RESULT

        <p class="note">
            Practice estimate from synthetic data. Yeh real market valuation
            ya verified sale price nahi hai.
        </p>
    </section>
</main>
</body>
</html>"""


PAGE = PAGE.replace("LOCALITY_OPTIONS", options(LOCALITIES))


def make_prediction(house):
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
                    value = float(house[category] == category_value)
                    break

        features.append(float(value))

    if not (
        len(features)
        == len(model["means"])
        == len(model["stds"])
        == len(model["weights"])
    ):
        raise ValueError("Model feature sizes match nahi karte.")

    scaled = [
        (value - mean) / std
        for value, mean, std in zip(
            features,
            model["means"],
            model["stds"],
        )
    ]

    price_lakh = (
        model["bias"]
        + sum(
            weight * value
            for weight, value in zip(model["weights"], scaled)
        )
    ) * model["target_std_lakh"] + model["target_mean_lakh"]

    return price_lakh * 100_000


def validate(house):
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
    ratio = (
        house["plot_area_sqft"] / builtup
        if builtup > 0
        else 0
    )

    if house["property_type"] == "Apartment":
        floors_ok = 3 <= house["total_floors"] <= 12
        area_ok = 0.90 <= ratio <= 1.12
    else:
        floors_ok = 1 <= house["total_floors"] <= 3
        area_ok = 0.85 <= ratio <= 1.60

    if not floors_ok:
        issues.append(
            "Is property type ke floors training data ki range se bahar hain."
        )

    if not 0 <= house["floor_number"] < house["total_floors"]:
        issues.append("Floor number total floors se kam hona chahiye.")

    if not area_ok:
        issues.append(
            "Plot/built-up area ratio training data ki range se bahar hai."
        )

    return issues


class PredictorHandler(BaseHTTPRequestHandler):
    def send_page(self, page):
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self.send_page(PAGE.replace("RESULT", ""))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        form_data = self.rfile.read(length).decode("utf-8")
        form = parse_qs(form_data)

        try:
            numeric_fields = [
                "bedrooms",
                "bathrooms",
                "builtup_area_sqft",
                "plot_area_sqft",
                "property_age_years",
                "floor_number",
                "total_floors",
            ]

            house = {
                key: float(form[key][0])
                for key in numeric_fields
            }

            for key in [
                "locality",
                "property_type",
                "parking",
                "furnishing",
            ]:
                house[key] = form[key][0]

            issues = validate(house)

            if issues:
                result = (
                    '<div class="error"><b>Input check nahi hua:</b><ul>'
                )
                result += "".join(
                    f"<li>{issue}</li>"
                    for issue in issues
                )
                result += "</ul></div>"
            else:
                price = make_prediction(house)

                if price < 0:
                    result = (
                        '<div class="error">'
                        "Is input par valid estimate nahi mila."
                        "</div>"
                    )
                else:
                    result = (
                        '<div class="result">'
                        f"Estimated practice price: ₹{price:,.0f}"
                        "</div>"
                    )

        except (KeyError, ValueError):
            result = (
                '<div class="error">'
                "Form mein valid values enter karein."
                "</div>"
            )

        self.send_page(PAGE.replace("RESULT", result))


server = HTTPServer(("127.0.0.1", 8000), PredictorHandler)

print("App chal rahi hai: http://127.0.0.1:8000")
print("Band karne ke liye terminal mein Ctrl+C dabayein.")

server.serve_forever()