import os
import csv

# === PATHS ===
BASE_DIR = r"D:\study\nlp\TAL\TP4\TP\All-in-many_classification"
OUTPUT_FILE = r"C:\Users\Imane\OneDrive\Bureau\TAL\TP4\article_labels\article_labels.csv"

# === MAP CLASS NUMBERS TO NAMES ===
LABEL_MAP = {
    "1": "Metaheuristics",
    "2": "Machine & Deep Learning",
    "3": "Combination of Metaheuristics & Machine/Deep Learning",
    "4": "Others"
}

# === COLLECT DATA ===
rows = []

for file in sorted(os.listdir(BASE_DIR)):
    file_path = os.path.join(BASE_DIR, file)

    # Skip if not a file
    if not os.path.isfile(file_path):
        continue

    article_number = file  # filename = article name (no extension)

    # Read the class label (1–4) from the file content
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            label = f.read().strip()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            label = f.read().strip()

    if label in LABEL_MAP:
        label_name = LABEL_MAP[label]
        rows.append([article_number, int(label), label_name])
    else:
        print(f"⚠️ Skipped {file} — invalid label content: '{label}'")

# === SAVE RESULTS TO CSV ===
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Article_Number", "Class_Label", "Label_Name"])
    writer.writerows(rows)

print(f"✅ File created successfully: {OUTPUT_FILE}")
