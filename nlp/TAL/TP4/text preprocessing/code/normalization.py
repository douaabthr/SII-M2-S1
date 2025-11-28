import os
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

# === PATHS ===
BASE_DIR = r"D:\study\nlp\TAL\TP4\text preprocessing"
TOKENS_DIR = os.path.join(BASE_DIR, "Tokens")
VOCAB_DIR = os.path.join(BASE_DIR, "Vocabulary")

# === STEMMERS ===
STEMMERS = {
    "Lancaster": LancasterStemmer(),
    "Porter": PorterStemmer(),
    "Snowball": SnowballStemmer("english")
}

# === CREATE OUTPUT FOLDERS ===
for stem_name in STEMMERS.keys():
    os.makedirs(os.path.join(BASE_DIR, stem_name, "Normalized_Tokens"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, stem_name, "Normalized_Vocabulary"), exist_ok=True)

# === GET ALL TOKEN FILES ===
token_files = [f for f in os.listdir(TOKENS_DIR) if f.endswith("_T.txt")]

if not token_files:
    print(f"⚠️ No token files found in {TOKENS_DIR}")
else:
    print(f"🔹 Found {len(token_files)} token files to stem.")

# === PROCESS EACH TOKEN FILE ===
for file in sorted(token_files):
    file_path = os.path.join(TOKENS_DIR, file)

    print(f"\n📄 Processing {file}...")

    # === READ TOKENS ===
    with open(file_path, "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]

    # === APPLY STEMMERS ===
    for stem_name, stemmer in STEMMERS.items():
        norm_tokens_dir = os.path.join(BASE_DIR, stem_name, "Normalized_Tokens")
        norm_vocab_dir = os.path.join(BASE_DIR, stem_name, "Normalized_Vocabulary")
        os.makedirs(norm_tokens_dir, exist_ok=True)
        os.makedirs(norm_vocab_dir, exist_ok=True)

        # Apply stemming (skip <s> and </s>)
        stemmed_tokens = [stemmer.stem(t) if t not in ["<s>", "</s>"] else t for t in tokens]
        stemmed_vocab = sorted(set(stemmed_tokens))

        # === SAVE RESULTS ===
        norm_tokens_file = os.path.join(norm_tokens_dir, file)
        norm_vocab_file = os.path.join(norm_vocab_dir, file.replace("_T.txt", "_V.txt"))

        with open(norm_tokens_file, "w", encoding="utf-8") as f:
            f.write("\n".join(stemmed_tokens))

        with open(norm_vocab_file, "w", encoding="utf-8") as f:
            f.write("\n".join(stemmed_vocab))

    print(f"   ✅ {file} stemmed with Lancaster, Porter, and Snowball")

print("\n🎉 All stemming completed successfully!")
