

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer,LancasterStemmer
import os
from collections import Counter
import math
from nltk.corpus import stopwords
import numpy as np

#==============QUERY PREPROCESSING ==============

queries = {
    "q1": "large language models for information retrieval and ranking",
    "q2": "LLM for information retrieval and Ranking",
    "q3": "query Reformulation in information retrieval",  
    "q4": "ranking Documents",
    "q5": "Optimizing recommendation systems with LLMs by leveraging item metadata"
}

ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    # Abbreviations like D.Z.A
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       # Words combined with numbers, e.g., data-
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          # Numbers with decimals, separators, or percentages
    r'|[A-Za-z]+'                         # Simple words (alphabetic)
) 


stopwords=stopwords.words('english')
porter=PorterStemmer()

processed_queries = {}

for qid, qtext in queries.items():
    tokens = ExpReg.tokenize(qtext)                        # Tokenize
    nostop_tokens = [t for t in tokens if t.lower() not in stopwords]  # Remove stopwords
    stemmed_tokens = [porter.stem(t) for t in nostop_tokens]               # Stem
    processed_queries[qid] = stemmed_tokens


# for qid, tokens in processed_queries.items():
#     print(f"{qid} tokens:", tokens)




#=============== CREATING TERM WEIGHT VECTORS===========


index = {}  # term -> dict of doc_id -> weight

with open("C:/Users/Imane/OneDrive/Bureau/ri/TP2/inverted_index_regex_porter.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
       
        term = parts[0]
        doc_id = parts[1]

        weight = float(parts[3])
        
        if term not in index:
            index[term] = {}
        index[term][doc_id] = weight

# ======= DOCUMENT VECTORS 

all_docs = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6']
doc_vectors = {}

for doc in all_docs:
    vector = []
    for term in index:
        # use weight if term appears in doc, otherwise 0
        vector.append(index[term].get(doc, 0.0))
    doc_vectors[doc] = vector


# print("Document vectors:")
# for doc, vec in doc_vectors.items():
#     print(f"{doc}: {vec}")


# ======= QUERY VECTORS

binary_query_vectors = {}

for qid, tokens in processed_queries.items():
    vector = [1 if term in tokens else 0 for term in index]
    binary_query_vectors[qid] = vector

# for qid, vec in binary_query_vectors.items():
#     print(f"{qid} binary vector:", vec)




#=============== COMPUTING SIMILARITY===========

def inner_product(query_vec, doc_vec):
    return np.dot(query_vec, doc_vec)

def cosine_similarity(query_vec, doc_vec):
    q = np.array(query_vec)
    d = np.array(doc_vec)
    numerator = np.dot(q, d)
    denominator = np.sqrt(np.sum(q ** 2) * np.sum(d ** 2))
    
    if denominator == 0: 
        return 0.0
    
    return numerator / denominator

def jaccard_similarity(query_vec, doc_vec):
    q = np.array(query_vec)
    d = np.array(doc_vec)
    numerator = np.dot(q, d)

    denominator=np.sum(d** 2) + np.sum(q ** 2)-np.dot(q, d)
    return numerator / denominator



similarity_methods = {
    "Inner Product": inner_product,
    "Cosine": cosine_similarity,
    "Jaccard": jaccard_similarity
}

results = {}  

for method_name, sim_func in similarity_methods.items():
    results[method_name] = {}
    for qid, q_vec in binary_query_vectors.items():
        scores = {}
        for doc_id, d_vec in doc_vectors.items():
            score = sim_func(q_vec, d_vec)
            scores[doc_id] = score
        # Sort documents by score descending
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results[method_name][qid] = sorted_docs

# ================== Print ranked documents ==================
for method_name in similarity_methods:
    print(f"\n=== Ranking using {method_name} ===")
    for qid, ranked_docs in results[method_name].items():
        print(f"\nQuery {qid} ranking:")
        for doc_id, score in ranked_docs:
            print(f"{doc_id}: {score:.4f}")
