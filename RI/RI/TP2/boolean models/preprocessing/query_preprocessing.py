

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer,LancasterStemmer
import os
from collections import Counter
import math



q = "(query AND reformulation) OR (Language AND model) "

ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    # Abbreviations like D.Z.A
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       # Words combined with numbers, e.g., data-
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          # Numbers with decimals, separators, or percentages
    r'|[A-Za-z]+'                         # Simple words (alphabetic)
) 

tokens=ExpReg.tokenize(q)

nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords=stopwords.words('english')


nostop_tokens=[t for t in tokens if t.lower() not in stopwords]
porter=PorterStemmer()
porter_tokens=[porter.stem(t) for t in nostop_tokens]

base_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP2/boolean models/preprocessing"
filename = os.path.join(base_folder, f"query_tokens.txt")
with open(filename, "w", encoding="utf-8") as f:
        for token in porter_tokens:
            f.write(f"{token}\n")
    
print(f"Inverted index saved successfully")
