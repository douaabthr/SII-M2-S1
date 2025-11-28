import nltk
from nltk.corpus import stopwords
import os

with open("TP1/exo1/text extraction/D_21.txt", "r", encoding="utf-8") as f:
    text = f.read()
stop_words= stopwords.words('english')
ExpReg = nltk.RegexpTokenizer(
    r'<\/?s>'                              # <k> or </k> sentence tags
    r'|(?:[A-Za-z]\.)+'                       # Abbreviations like D.Z.A
    r'|[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'  # scientific notation e.g. 0.9184e+05
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'          # Words with numbers, e.g., data-2
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'             # Numbers, decimals, %, etc.
    r'|[A-Za-z]+'                            # Simple words
)

terms= ExpReg.tokenize(text)
terms_no_stop= [t for t in terms if t.lower() not in stop_words]

save_dir = "TP1/exo1/text preprocessing"
filename = os.path.join(save_dir, f"T.txt")
with open(filename, "w", encoding="utf-8") as f:
    for term in terms_no_stop:
        f.write(f"{term}\n")

print(f"Saved tokens {filename}")


vocab = sorted(set(terms))

filename = os.path.join(save_dir, f"V.txt")
with open(filename, "w", encoding="utf-8") as f:
    for term in vocab:
        f.write(f"{term}\n")
print(f"Saved vocab {filename}")
