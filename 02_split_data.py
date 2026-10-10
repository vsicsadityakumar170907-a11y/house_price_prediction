import csv
import random

with open("data/kanpur_house_prices.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

random.Random(42).shuffle(rows)

split_index = int(len(rows) * 0.8)
train_rows = rows[:split_index]
test_rows = rows[split_index:]

columns = rows[0].keys()

for filename, dataset in [
    ("data/train.csv", train_rows),
    ("data/test.csv", test_rows),
]:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(dataset)

print("Training records:", len(train_rows))
print("Testing records:", len(test_rows))