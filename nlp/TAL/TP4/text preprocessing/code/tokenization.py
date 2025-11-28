import nltk
import os
import re
from nltk.corpus import stopwords

# === Setup ===
nltk.download('stopwords', quiet=True)

BASE_DIR = r"D:\study\nlp\TAL\TP4\TP\All-in-many"
TOKENS_DIR = r"D:\study\nlp\TAL\TP4\text preprocessing\Tokens"
VOCAB_DIR = r"D:\study\nlp\TAL\TP4\text preprocessing\Vocabulary"

os.makedirs(TOKENS_DIR, exist_ok=True)
os.makedirs(VOCAB_DIR, exist_ok=True)

stop_words = set(stopwords.words('english'))

# === Tokenizer ===

pattern = r'(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[.,\-]\d+)?%?|\w+(?:[-/]\w+)*|[.!?]+'

tokenizer = nltk.RegexpTokenizer(pattern)

def natural_sort_key(name):
    return [int(s) if s.isdigit() else s.lower() for s in re.split(r'(\d+)', name)]

# === Process all article files ===
files = sorted(
    [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))],
    key=natural_sort_key
)

if not files:
    print("⚠️ No article files found in:", BASE_DIR)
else:
    print(f"🔹 Found {len(files)} article files to process.")

for file in files:
    file_path = os.path.join(BASE_DIR, file)

    print(f"\n📄 Processing {file}...")

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()
    except Exception as e:
        print(f"   ❌ Error reading {file}: {e}")
        continue

    if not text:
        print(f"   ⚠️ File is empty, skipping: {file}")
        continue

    # Tokenize & remove stopwords
    tokens = tokenizer.tokenize(text)
    tokens_no_stop = [t for t in tokens if t.lower() not in stop_words]
    vocab = sorted(set(tokens_no_stop))

    # Save tokens and vocab
    tokens_file = os.path.join(TOKENS_DIR, f"{file}_T.txt")
    vocab_file = os.path.join(VOCAB_DIR, f"{file}_V.txt")

    with open(tokens_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tokens_no_stop))

    with open(vocab_file, "w", encoding="utf-8") as f:
        f.write("\n".join(vocab))

    print(f"   ✅ Saved tokens → {tokens_file}")
    print(f"   ✅ Saved vocab → {vocab_file}")

print("\n🎉 All articles processed successfully!")

