import nltk 
import os

with open("TP1/exo1/text preprocessing/T.txt", "r", encoding="utf-8") as f:
    tokens = f.read()


stemmer = nltk.SnowballStemmer("english") 

tokens = tokens.lower()  
tokens = nltk.word_tokenize(tokens) 

save_dir = "TP1/exo1/text preprocessing"
filename = os.path.join(save_dir, f"T_N.txt")
with open(filename, "w", encoding="utf-8") as f:
    for term in tokens:
        f.write(f"{term}\n")

print(f"Saved tokens {filename}")

vocab = sorted(set(tokens))

filename = os.path.join(save_dir, f"V_N.txt")
with open(filename, "w", encoding="utf-8") as f:
    for term in vocab:
        f.write(f"{term}\n")
print(f"Saved vocab {filename}")
    