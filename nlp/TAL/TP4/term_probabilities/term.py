import os
import csv
from collections import Counter, defaultdict

# === PATHS ===
CLASS_DIR = r"D:\study\nlp\TAL\TP4\TP\All-in-many_classification"

TOKENS_PATHS = {
    "Original": r"D:\study\nlp\TAL\TP4\text preprocessing\Tokens",
    "Lancaster": r"D:\study\nlp\TAL\TP4\text preprocessing\Lancaster\Normalized_Tokens",
    "Porter": r"D:\study\nlp\TAL\TP4\text preprocessing\Porter\Normalized_Tokens",
    "Snowball": r"D:\study\nlp\TAL\TP4\text preprocessing\Snowball\Normalized_Tokens"
}

OUTPUT_DIR = r"D:\study\nlp\TAL\TP4\term_probabilities"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === LOAD ARTICLE LABELS ===
article_class = {}
for file in os.listdir(CLASS_DIR):
    file_path = os.path.join(CLASS_DIR, file)
    if os.path.isfile(file_path):
        article_number = file  # filename = article number
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            label = f.read().strip()
            if label in {"1", "2", "3", "4"}:
                article_class[article_number] = int(label)
            else:
                print(f"⚠️ Skipped {file} — invalid label: '{label}'")

print(f"Loaded {len(article_class)} article labels.\n")

# === FUNCTION TO CALCULATE P(w|c) ===
def calculate_word_probs(tokens_dir, output_file):
    class_word_counts = defaultdict(Counter)
    class_total_words = Counter()
    vocab = set()

    for root, _, files in os.walk(tokens_dir):
        for file in files:
            if not file.endswith("_T.txt"):
                continue
            file_path = os.path.join(root, file)

            # Strip _T.txt to get the article number
            article_number = file[:-6]  # removes "_T.txt"

            class_label = article_class.get(article_number)
            if not class_label:
                continue  # skip if no class found

            # Read tokens
            with open(file_path, "r", encoding="utf-8") as f:
                tokens = [line.strip() for line in f if line.strip()]

            if not tokens:
                continue

            print(f"Processing {file}: class {class_label}, tokens {len(tokens)}")
            vocab.update(tokens)
            class_word_counts[class_label].update(tokens)
            class_total_words[class_label] += len(tokens)

    vocab = sorted(vocab)
    V = len(vocab)

    # Write probabilities
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Term", "P(class1)", "P(class2)", "P(class3)", "P(class4)"])
        for term in vocab:
            probs = []
            for c in range(1, 5):
                count = class_word_counts[c].get(term, 0)
                total = class_total_words[c]
                prob = (count + 1) / (total + V)  # Laplace smoothing
                probs.append(round(prob, 4))
            writer.writerow([term] + probs)

# === PROCESS ALL TOKEN TYPES ===
for name, path in TOKENS_PATHS.items():
    output_file = os.path.join(OUTPUT_DIR, f"word_probs_{name}.csv")
    print(f"\nProcessing {name} tokens...")
    calculate_word_probs(path, output_file)
    print(f"✅ Saved: {output_file}")

print("\n🎉 All word probabilities computed successfully!")
