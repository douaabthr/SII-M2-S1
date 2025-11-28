import os
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

# === PATHS ===
OUTPUT_DIR = "D:/study/nlp/TAL/TP2/text preprocessing"
TOKENS_DIR = os.path.join(OUTPUT_DIR, "Tokens")
VOCAB_DIR = os.path.join(OUTPUT_DIR, "Vocabulary")

# === STEMMERS ===
STEMMERS = {
    "Lancaster": LancasterStemmer(),
    "Porter": PorterStemmer(),
    "Snowball": SnowballStemmer("english")
}

# === CREATE OUTPUT FOLDERS ===
for stem_name in STEMMERS.keys():
    os.makedirs(os.path.join(OUTPUT_DIR, stem_name, "Normalized_Tokens"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, stem_name, "Normalized_Vocabulary"), exist_ok=True)

# === PROCESS EACH VOLUME ===
for volume in sorted(os.listdir(TOKENS_DIR)):
    volume_tokens_dir = os.path.join(TOKENS_DIR, volume)
    volume_vocab_dir = os.path.join(VOCAB_DIR, volume)

    if not os.path.isdir(volume_tokens_dir):
        continue

    print(f"\n🔹 Processing {volume}...")

    for file in sorted(os.listdir(volume_tokens_dir)):
        if not file.endswith("_T.txt"):
            continue

        # === READ TOKENS ===
        with open(os.path.join(volume_tokens_dir, file), "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]

        # === APPLY STEMMERS ===
        for stem_name, stemmer in STEMMERS.items():
            norm_tokens_dir = os.path.join(OUTPUT_DIR, stem_name, "Normalized_Tokens", volume)
            norm_vocab_dir = os.path.join(OUTPUT_DIR, stem_name, "Normalized_Vocabulary", volume)
            os.makedirs(norm_tokens_dir, exist_ok=True)
            os.makedirs(norm_vocab_dir, exist_ok=True)

            # Apply stemming (skip sentence tags)
            stemmed_tokens = [stemmer.stem(t) if t not in ["<s>", "</s>"] else t for t in tokens]
            stemmed_vocab = sorted(set(stemmed_tokens))

            # === SAVE RESULTS ===
            norm_tokens_file = os.path.join(norm_tokens_dir, file)
            norm_vocab_file = os.path.join(norm_vocab_dir, file.replace("_T.txt", "_V.txt"))

            with open(norm_tokens_file, "w", encoding="utf-8") as f:
                f.write("\n".join(stemmed_tokens))

            with open(norm_vocab_file, "w", encoding="utf-8") as f:
                f.write("\n".join(stemmed_vocab))

        print(f"  ✅ {file} → stemmed with all stemmers")

print("\n🎉 All stemming completed successfully!")
