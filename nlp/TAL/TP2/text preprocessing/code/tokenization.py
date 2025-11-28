import nltk
import os
import re
from nltk.corpus import stopwords

# Make sure stopwords are downloaded
nltk.download('stopwords')

# === PATHS ===
BASE_DIR = "D:/study/nlp/TAL/TP2/text extraction"
TOKENS_DIR = "D:/study/nlp/TAL/TP2/text preprocessing/Tokens"
VOCAB_DIR = "D:/study/nlp/TAL/TP2/text preprocessing/Vocabulary"

os.makedirs(TOKENS_DIR, exist_ok=True)
os.makedirs(VOCAB_DIR, exist_ok=True)

# === STOPWORDS & TOKENIZER ===
stop_words = set(stopwords.words('english'))

# Regular expression including commas and sentence tags <s> </s>

ExpReg = nltk.RegexpTokenizer(r'<\/?s>|(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[.,\-]\d+)?%?|\w+(?:[-/]\w+)*|[.!?]+')


# === PROCESS ALL VOLUMES ===
for volume in sorted(os.listdir(BASE_DIR)):
    volume_path = os.path.join(BASE_DIR, volume)
    if not os.path.isdir(volume_path):
        continue

    print(f"\n🔹 Processing {volume}...")

    # Create subfolders
    volume_tokens_dir = os.path.join(TOKENS_DIR, volume)
    volume_vocab_dir = os.path.join(VOCAB_DIR, volume)
    os.makedirs(volume_tokens_dir, exist_ok=True)
    os.makedirs(volume_vocab_dir, exist_ok=True)

    for file in sorted(os.listdir(volume_path), key=lambda x: int(x.split('.')[0])):
        file_path = os.path.join(volume_path, file)

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()

        # === STEP 1: Add </s> after title ===
        # Assuming the title ends at the first newline (\n)
        text = re.sub(r'^(.*?)(\r?\n)', r'\1 </s> <s> ', text, count=1, flags=re.DOTALL)

        # === STEP 2: Mark sentence boundaries ===
        # Add </s> <s> between sentences
        text = re.sub(r'\s*([.!?])\s+', r' </s> <s> ', text)
        text = "<s> " + text.strip()
        if not text.endswith("</s>"):
            text += " </s>"

        # === STEP 3: Tokenize ===
        terms_no_stop = ExpReg.tokenize(text)

        # === STEP 4: Vocabulary ===
        vocab = sorted(set(terms_no_stop))

        # === Save Tokens ===
        tokens_file = os.path.join(volume_tokens_dir, f"{file.replace('.txt', '')}_T.txt")
        with open(tokens_file, "w", encoding="utf-8") as f:
            f.write("\n".join(terms_no_stop))

        # === Save Vocabulary ===
        vocab_file = os.path.join(volume_vocab_dir, f"{file.replace('.txt', '')}_V.txt")
        with open(vocab_file, "w", encoding="utf-8") as f:
            f.write("\n".join(vocab))

        print(f"  ✅ {file} → Saved tokens and vocab")

print("\n🎉 All volumes processed successfully!")
