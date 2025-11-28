import os
import csv
from collections import Counter

# === PATHS ===
BASE_DIR = r"D:\study\nlp\TAL\TP4\TP\All-in-many_classification"
OUTPUT_FILE = r"D:\study\nlp\TAL\TP4\class_probabilities\class_probabilities.csv"

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# === MAP CLASS NUMBERS TO NAMES ===
LABEL_MAP = {
    "1": "Metaheuristics",
    "2": "Machine & Deep Learning",
    "3": "Combination of Metaheuristics & Machine/Deep Learning",
    "4": "Others"
}

# === COLLECT CLASS LABELS ===
labels = []

for file in os.listdir(BASE_DIR):
    file_path = os.path.join(BASE_DIR, file)
    if not os.path.isfile(file_path):
        continue

    # Read label from file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            label = f.read().strip()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            label = f.read().strip()

    if label in LABEL_MAP:
        labels.append(label)
    else:
        print(f"⚠️ Skipped {file} — invalid label content: '{label}'")

# === CALCULATE PROBABILITIES ===
total_docs = len(labels)
counter = Counter(labels)

probabilities = []
for label, name in LABEL_MAP.items():
    count = counter.get(label, 0)
    prob = round(count / total_docs, 4) if total_docs > 0 else 0
    probabilities.append([int(label), name, count, prob])

# === SAVE TO CSV ===
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Class_Label", "Label_Name", "Document_Count", "P(c)"])
    writer.writerows(probabilities)

print(f"✅ Class probabilities saved to {OUTPUT_FILE}")
