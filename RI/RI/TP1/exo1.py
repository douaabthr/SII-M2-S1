# -*- coding: utf-8 -*-"


### steps:
# basically kept the terms in 4 dicts (tok, stem) each containg 6 dicts with each doc and
#its terms
    # freq and wights of inverted : using term files : match the doc and tok stem type and copy values
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer,LancasterStemmer
import os
from collections import Counter
import math

# ******************** EXO1 ********************
# **********************************************

##### reading files

documents={}
for file in os.listdir("C:/Users/Imane/OneDrive/Bureau/ri/TP1/Collection"):
    if file.endswith(".txt"):
        doc_id=file.split(".")[0]
        with open(os.path.join("C:/Users/Imane/OneDrive/Bureau/ri/TP1/Collection",file),"r",encoding="utf-8") as f:
            documents[doc_id]=f.read()
            print(documents[doc_id])
            
##### I.building the index

## 1.term extraction

split_terms={}
regex_terms={}

# ExpReg=RegexpTokenizer(r'(?:[A-Z]\.)+|\d+(?:\.\d+)?[A-Za-z]*|\w+|\.{3}')
ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    # Abbreviations like D.Z.A
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       # Words combined with numbers, e.g., data-
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          # Numbers with decimals, separators, or percentages
    r'|[A-Za-z]+'                         # Simple words (alphabetic)
) 
#(?:[A-Z]\.)i  --> group of eltters. repeated OR
# digits with mzybe deciaml and maybe letter OR
# words OR
# ellipses ...

for doc in documents:
    split_terms[doc]=documents[doc].split()
    # print(split_terms[doc])
    
    regex_terms[doc]=ExpReg.tokenize(documents[doc])
    # print(regex_terms[doc])

## 2.removing stopwords

nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords=stopwords.words('english')

split_nostop_terms={}
regex_nostop_terms={}

for doc in documents:
    split_nostop_terms[doc]=[t for t in split_terms[doc] if t.lower() not in stopwords]
    # print(split_nostop_terms[doc])
    
    regex_nostop_terms[doc]=[t for t in regex_terms[doc] if t.lower() not in stopwords]
    # print(regex_nostop_terms[doc])


## 3.normalisation

porter=PorterStemmer()
lancaster=LancasterStemmer()

porter_split_nostop_terms={}
lancaster_split_nostop_terms={}

porter_regex_nostop_terms={}
lancaster_regex_nostop_terms={}

for doc in documents:
    porter_split_nostop_terms[doc]=[porter.stem(t) for t in split_nostop_terms[doc]]
    porter_regex_nostop_terms[doc]=[porter.stem(t) for t in regex_nostop_terms[doc]]
    lancaster_split_nostop_terms[doc]=[lancaster.stem(t) for t in split_nostop_terms[doc]]
    lancaster_regex_nostop_terms[doc]=[lancaster.stem(t) for t in regex_nostop_terms[doc]]
   
    
## 4. Create document-term files


base_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP1/Terms"

index_versions = {
    "split_porter": porter_split_nostop_terms,
    "regex_porter": porter_regex_nostop_terms,
    "split_lancaster": lancaster_split_nostop_terms,
    "regex_lancaster": lancaster_regex_nostop_terms
}

for name, terms_dict in index_versions.items():
    print(name)
    print("******")
    output_folder = os.path.join(base_folder, f"Terms_{name}")
    os.makedirs(output_folder, exist_ok=True)

    # === document frequency ===
    doc_freq = {}
    for doc, terms in terms_dict.items():
        for term in set(terms):  # count once per doc
            doc_freq[term] = doc_freq.get(term, 0) + 1

    N = len(terms_dict)  # total number of documents
    
    # === TF-IDF ===
    for doc, terms in terms_dict.items():
        term_freq = Counter(terms)
        max_freq = max(term_freq.values())  # maximum frequency in that doc

        # Sort: numerics first, then alphabetically
        sorted_terms = sorted(term_freq.items(), key=lambda x: (not x[0].isdigit(), x[0]))

        output_path = os.path.join(output_folder, f"{doc}.txt")
        
        print("DOC",doc)
        print("*****")
        with open(output_path, "w", encoding="utf-8") as f:
            for term, freq in sorted_terms:
                tf = freq / max_freq
                idf = math.log10((N / doc_freq[term]) + 1)
                tfidf = tf * idf
                print(term,tf,idf)
                f.write(f"{doc} {term} {freq} {tfidf:.6f}\n")

    print(f"Term files with TF-IDF (normalized by max freq) created successfully in: {output_folder}")
    
## 5. Create inverted index-files


output_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP1/Inverted index"

for name, terms_dict in index_versions.items():
    # Use a set to remove duplicates
    rows_set = set()
    for doc_id, terms in terms_dict.items():
        for term in terms:
            rows_set.add((term, doc_id))
    
    # Convert set to list for sorting
    rows = list(rows_set)

    #  Use the same sorting logic as in the term files
    rows.sort(key=lambda x: (not x[0].isdigit(), x[0]))

    # Save to file
    output_path = os.path.join(output_folder, f"inverted_index_{name}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        for term, doc_id in rows:
            f.write(f"{term} {doc_id}\n")
    
    print(f"Inverted index saved successfully: {output_path}")


## adding frequncies and weights

import os

# Paths
terms_base_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP1/Terms"
inverted_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP1/Inverted index"

for name in index_versions.keys():
    print(f"\nUpdating inverted index for: {name}")

    inverted_path = os.path.join(inverted_folder, f"inverted_index_{name}.txt")
    updated_lines = []

    with open(inverted_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        term, doc_id = line.strip().split()

        # === Find matching term in the term file for that doc ===
        term_file_path = os.path.join(terms_base_folder, f"Terms_{name}", f"{doc_id}.txt")
        freq = None
        tfidf = None

        if os.path.exists(term_file_path):
            with open(term_file_path, "r", encoding="utf-8") as tf:
                for l in tf:
                    parts = l.strip().split()
                    if len(parts) >= 4 and parts[1] == term:  # doc term freq tfidf
                        freq = parts[2]
                        tfidf = parts[3]
                        break

        if freq is not None and tfidf is not None:
            updated_lines.append(f"{term} {doc_id} {freq} {tfidf}\n")
        else:
            # In case not found — keep as is but mark missing
            updated_lines.append(f"{term} {doc_id} 0 0.0\n")

    # === Overwrite the same file with updated content ===
    with open(inverted_path, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f" Updated inverted index file: {inverted_path}")

