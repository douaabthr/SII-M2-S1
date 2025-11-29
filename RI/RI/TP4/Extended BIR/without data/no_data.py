import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))  
from collections import defaultdict

# ========== doc with terms==========

docs = defaultdict(dict)


with open(r"C:\Users\Imane\OneDrive\Bureau\ri\TP4\inverted_index_regex_porter.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4:
            term, doc_id,  freq, weight = parts
            docs[doc_id][term] = float(weight)
print(docs)
#=========query preprocessing===========
queries = [
    "large language models for information retrieval and ranking",
    "LLM for information retrieval and Ranking",
    "query Reformulation in information retrieval",
    "ranking Documents",
    "Optimizing recommendation systems with LLMs by leveraging item metadata "

]


ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                   
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          
    r'|[A-Za-z]+'                         
)

stop_words = set(stopwords.words('english'))


stemmer = PorterStemmer()


preprocessed_queries = []

for q in queries:
    tokens = ExpReg.tokenize(q.lower())           
    tokens = [t for t in tokens if t not in stop_words]  
    tokens = [stemmer.stem(t) for t in tokens]    
    preprocessed_queries.append(tokens)


for i, tokens in enumerate(preprocessed_queries, 1):
    print(f"Q{i}:", tokens)


#========RSV=========

import numpy as np

# N and n_i

#N = number of docs
N = len(docs) 

# n_i = number of docs containing each term
term_doc_count = defaultdict(int)
for doc_id, terms in docs.items():
    for term in terms:
        term_doc_count[term] += 1   # cuz each term only appears once in each document in the index!!!!

# Compute RSV per query 
for qi, query_tokens in enumerate(preprocessed_queries, 1):
    print(f"\n=== Query {qi} ===")
    rsv_scores = {} 
    
    for doc_id, terms in docs.items():
        # intersection query and doc
        common_terms = set(query_tokens) & set(terms.keys())
       
        # print(doc_id,common_terms)
       
        rsv = 0.0
        for term in common_terms:
            ni = term_doc_count[term] # dict containing 
            wt = terms[term]
            idf = np.log10((N - ni + 0.5) / (ni + 0.5))
            
            rsv += wt * idf
        
        
        
        rsv_scores[doc_id] = rsv
    

    sorted_docs = sorted(rsv_scores.items(), key=lambda x: x[1], reverse=True)
    for doc, score in sorted_docs:  # top 5 docs
        print(f"{doc}: {score:.6f}")
