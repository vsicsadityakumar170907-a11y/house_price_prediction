import csv
from collections import Counter

with open("data/kanpur_house_prices.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

print("Total records:", len(rows))
print("Columns:", list(rows[0].keys()))
print("First 3 records:")
for row in rows[:3]:
    print(row)

print("Locality-wise records:")
print(Counter(row["locality"] for row in rows))
ids = [row["record_id"] for row in rows]
prices = [int(row["price_inr"]) for row in rows]

print("\nDuplicate IDs:", len(ids) - len(set(ids)))
print("Missing values:", sum(
    1 for row in rows
    for value in row.values()
    if value == ""
))
print("Minimum price: ₹", min(prices))
print("Maximum price: ₹", max(prices))