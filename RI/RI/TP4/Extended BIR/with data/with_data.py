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

# compute N and n_i 
N = len(docs)  
print(N)
# n_i = number of docs containing each term
term_doc_count = defaultdict(int)
for doc_id, terms in docs.items():
    for term in terms:
        term_doc_count[term] += 1 # cuz each term only appears once in each document in the index!!!!

# ---------- 2. Compute RSV per query ----------
relevant_docs = {
    "q1": ["D2", "D4"],
    "q2": ["D2", "D4"],
    "q3": ["D4", "D1"],
    "q4": ["D2", "D1"],
    "q5": ["D3", "D6"]
}
for qi, query_tokens in enumerate(preprocessed_queries, 1):
    qname = f"q{qi}"
    print(f"\n=== Query {qname} ===")
    relevant = relevant_docs.get(qname, [])

    R = len(relevant)  
    
    rsv_scores = {}

    for doc_id, terms in docs.items():
        common_terms = set(query_tokens) & set(terms.keys())
        # print(doc_id,common_terms)
        rsv = 0.0
        for term in common_terms:
            ni = term_doc_count[term]
            
            # r_i  number of relevant docs that contain term
            ri = sum(1 for d in relevant if term in docs[d])
            
           
            numerator = (ri + 0.5) / (R - ri + 0.5)
            denominator =  (ni - ri + 0.5)/(N - ni - R + ri + 0.5)
            if denominator > 0 and numerator > 0:
                idf_prob = np.log10(numerator / denominator)
            else:
                idf_prob = 0.0
            
            wt = terms[term]
            
            rsv += wt*idf_prob
        
        rsv_scores[doc_id] = rsv
 
    sorted_docs = sorted(rsv_scores.items(), key=lambda x: x[1], reverse=True)
    
    for doc, score in sorted_docs:
        print(f"  {doc}: {score:.6f}")
