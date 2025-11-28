import os

# === PATHS ===
BASE_PREPROC = "D:/study/nlp/TAL/TP2/text preprocessing"

TOKENS_RAW_DIR = os.path.join(BASE_PREPROC, "Tokens")
NORMALIZED_DIRS = [
    os.path.join(BASE_PREPROC, "Lancaster/Normalized_Tokens"),
    os.path.join(BASE_PREPROC, "Porter/Normalized_Tokens"),
    os.path.join(BASE_PREPROC, "Snowball/Normalized_Tokens")
]

SENTENCES_DIR = os.path.join(BASE_PREPROC, "Sentences")
os.makedirs(SENTENCES_DIR, exist_ok=True)

def extract_sentences_from_tokens(tokens):
    """Group tokens into sentences based on <s> and </s> tags."""
    sentences = []
    current_sentence = []

    for token in tokens:
        if token == "<s>":
            current_sentence = []
        elif token == "</s>":
            if current_sentence:
                sentences.append(" ".join(current_sentence))
        else:
            current_sentence.append(token)
    return sentences


# === STEP 1: RAW TOKENS ===
print("\n🔹 Extracting sentences from RAW tokens...")
for volume in sorted(os.listdir(TOKENS_RAW_DIR)):
    volume_path = os.path.join(TOKENS_RAW_DIR, volume)
    if not os.path.isdir(volume_path):
        continue

    volume_sent_dir = os.path.join(SENTENCES_DIR, "Raw", volume)
    os.makedirs(volume_sent_dir, exist_ok=True)

    for file in sorted(os.listdir(volume_path)):
        if not file.endswith("_T.txt"):
            continue

        file_path = os.path.join(volume_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            tokens = [t.strip() for t in f if t.strip()]

        sentences = extract_sentences_from_tokens(tokens)

        out_path = os.path.join(volume_sent_dir, file.replace("_T.txt", "_S.txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sentences))

        print(f"  ✅ Raw → {file} → {len(sentences)} sentences")

# === STEP 2: NORMALIZED TOKENS (Lancaster, Porter, Snowball) ===
print("\n🔹 Extracting sentences from NORMALIZED tokens...")

for norm_dir in NORMALIZED_DIRS:
    if not os.path.exists(norm_dir):
        print(f"⚠️ Skipped missing directory: {norm_dir}")
        continue

    stemmer_name = os.path.basename(os.path.dirname(norm_dir))
    print(f"\nProcessing stemmer: {stemmer_name}")

    for volume in sorted(os.listdir(norm_dir)):
        volume_path = os.path.join(norm_dir, volume)
        if not os.path.isdir(volume_path):
            continue

        volume_sent_dir = os.path.join(SENTENCES_DIR, stemmer_name, volume)
        os.makedirs(volume_sent_dir, exist_ok=True)

        for file in sorted(os.listdir(volume_path)):
            if not file.endswith("_T.txt"):
                continue

            file_path = os.path.join(volume_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                tokens = [t.strip() for t in f if t.strip()]

            sentences = extract_sentences_from_tokens(tokens)

            out_path = os.path.join(volume_sent_dir, file.replace("_T.txt", "_S.txt"))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(sentences))

            print(f"  ✅ {stemmer_name} → {file} → {len(sentences)} sentences")

print("\n🎉 All raw and normalized sentences extracted successfully!")
