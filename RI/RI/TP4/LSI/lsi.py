import numpy as np
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))  # don't overwrite the module
#==========1.Build the TF–IDF Matrix 𝑊 ================

print("==========1.Build the TF–IDF Matrix 𝑊 ================")
index = {}

with open("C:/Users/Imane/OneDrive/Bureau/ri/TP2/inverted_index_regex_porter.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 4:
            continue  # skip malformed lines

        term = parts[0]
        doc_id = parts[1]
        weight = float(parts[3])

        if term not in index:
            index[term] = set()
        index[term].add((doc_id, weight))

print("Number of terms:", len(index))
print(index)
# Create a mapping of doc_ids to column indices
all_doc_ids = sorted({doc for postings in index.values() for doc, _ in postings})
doc_to_idx = {doc: i for i, doc in enumerate(all_doc_ids)}

# Initialize the term-document matrix
W = np.zeros((len(index), len(all_doc_ids)), dtype=float)

# Fill matrix with weights
for i, (term, postings) in enumerate(index.items()):
    for doc_id, weight in postings:
        j = doc_to_idx[doc_id]
        W[i, j] = weight

print("W Matrix shape:", W.shape)
print(W)
#==========2.SVD ================

print("==========2.SVD ================")
U, S, VT = np.linalg.svd(W, full_matrices=True) 
print("U Matrix shape:", U.shape)
print("S Matrix shape:", S.shape)
print("VT Matrix shape:", VT.shape)

#==========3. Dimensionality reduction ================

print("==========3. Dimensionality reduction ================")
k = 3  # target reduced dimension
U_k = U[:, :k]         # m x k
S_k = S[:k,]   # k x k
VT_k = VT[:k, :]       # k x n
print("U_k Matrix shape:", U_k.shape)
print("S_k Matrix shape:", S_k.shape)
print("VT_k Matrix shape:", VT_k.shape)

#==========4. Represent the queries as binary vectors================
print("==========4. Represent the queries as binary vectors================")
queries = [
    "large language models for information retrieval and ranking",
    "LLM for information retrieval and Ranking",
    "query Reformulation in information retrieval",
    "ranking Documents",
    "Optimizing recommendation systems with LLMs by leveraging item metadata "
]

# Tokenizer
ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    # Abbreviations like D.Z.A
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       # Words combined with numbers, e.g., data-
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          # Numbers with decimals, separators, or percentages
    r'|[A-Za-z]+'                         # Simple words (alphabetic)
)

# Stopwords
stop_words = set(stopwords.words('english'))

# Stemmer
stemmer = PorterStemmer()

# Preprocessing
preprocessed_queries = []

for q in queries:
    tokens = ExpReg.tokenize(q.lower())              # tokenize & lowercase
    tokens = [t for t in tokens if t not in stop_words]  # remove stopwords
    tokens = [stemmer.stem(t) for t in tokens]      # apply Porter stemmer
    preprocessed_queries.append(tokens)

# Print preprocessed queries
for i, tokens in enumerate(preprocessed_queries, 1):
    print(f"Q{i}:", tokens)

#  query vectors
terms_list = list(index.keys())          # ordered list of all terms
term_to_idx = {term: i for i, term in enumerate(terms_list)}

queries_vectors = []

for tokens in preprocessed_queries:
    binary_vector = np.zeros(len(terms_list), dtype=float)
    for t in tokens:
        if t in term_to_idx:
            idx = term_to_idx[t]
            binary_vector[idx] = 1
    queries_vectors.append(binary_vector)


#==========5. Query projection================
print("==========5. Query projection================")
S_k_diag = np.diag(S_k)         # k x k diagonal matrix
S_k_inv = np.linalg.inv(S_k_diag)  # inverse of the diagonal matrix

q_new_list = []

for i, q_vec in enumerate(queries_vectors, 1):  # <-- use queries_vectors, not binary_vector
   
    q_vec = np.asarray(q_vec).reshape(-1, 1)  # m x 1
    q_new = S_k_inv @ (U_k.T @ q_vec)         # k x 1
   
    q_new = q_new.flatten()                   # flatten to 1D
  
    q_new_list.append(q_new)
    print(f"Q{i} projected vector (Q{i}_new):", q_new)


#==========6. similarity matrices ================

print("==========6. similarity matrices ================")
similarity_matrices = []  # list of matrices, one per query

for i, q_new in enumerate(q_new_list, 1):
    q_new_col = q_new.reshape(1, -1)              # 1 x k
    # similarity matrix for this query
    sim_matrix = q_new_col @ (S_k_diag @ S_k_diag) @ VT_k  # 1 x n
    similarity_matrices.append(sim_matrix)
    
    print(f"Q{i} similarity values:", sim_matrix)

num_docs = 6  # assuming 6 documents

print("=== Similarity of each query to each document ===")
for i, sim_matrix in enumerate(similarity_matrices, 1):
    sim_scores = sim_matrix.flatten()[:num_docs]  # similarity to first 6 docs
    print(f"\nQuery {i}:")
    for doc_idx, score in enumerate(sim_scores, 1):  # 1-based doc numbering
        print(f"  Document {doc_idx}: similarity = {score:.4f}")

    
#==========6 Document ranking ================

num_docs = 6  # assuming 6 documents

print("=== Ranked similarity of each query to documents ===")
for i, sim_matrix in enumerate(similarity_matrices, 1):
    sim_scores = sim_matrix.flatten()[:num_docs]  # similarity to first 6 docs

    # rank documents (highest similarity first)
    ranked_indices = np.argsort(-sim_scores)  # descending order

    print(f"\nQuery {i} ranked documents:")
    for rank, doc_idx in enumerate(ranked_indices, 1):  # 1-based rank
        print(f" {rank}: D{doc_idx+1} with similarity = {sim_scores[doc_idx]:.4f}")
