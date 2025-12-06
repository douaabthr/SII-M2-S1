from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk

# ============================================
# 1) TELECHARGEMENT DES STOPWORDS
# ============================================
nltk.download('stopwords')

# ============================================
# 2) LECTURE INDEX INVERSÉ
# ============================================
docs = defaultdict(dict)

with open(r"D:\study\RI\RI\TP4\inverted_index_regex_porter.txt",
          "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 4:
            term, doc_id, freq, weight = parts
            docs[doc_id][term] = int(freq)

# ============================================
# 3) LONGUEUR DES DOCUMENTS
# ============================================
doc_lengths = {doc_id: sum(terms.values()) for doc_id, terms in docs.items()}

# ============================================
# 4) UNIGRAMMES NORMALISÉS PAR LONGUEUR DE CHAQUE DOC
# ============================================
unigram_normalized = defaultdict(dict)

for doc_id, term_freqs in docs.items():
    doc_len = doc_lengths[doc_id]
    for term, freq in term_freqs.items():
        unigram_normalized[doc_id][term] = freq / doc_len
        

# ============================================
# 5) TOKENIZER + STOPWORDS + STEMMER
# ============================================
ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          
    r'|[A-Za-z]+'                         
)

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))

def tokenize(text):
    tokens = ExpReg.tokenize(text.lower())
    tokens = [tok for tok in tokens if tok not in stop_words]  
    stems = [stemmer.stem(tok) for tok in tokens]              
    return stems

# ============================================
# 6) RANKING : PRODUIT DES UNIGRAMMES
# ============================================
print(unigram_normalized)
def rank_query_product(query, unigram_normalized):
    terms = tokenize(query)
    scores = {}

    for doc_id, term_freqs in unigram_normalized.items():
        score = 1.0  # produit commence à 1
        for t in terms:
            if t in term_freqs:
                print(t,doc_id,term_freqs[t])
                score *= term_freqs[t]
            else:
                score = 0  # si un terme manque, score = 0
                break
        scores[doc_id] = score

    # Tri décroissant
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

# ============================================
# 7) QUERIES
# ============================================
queries = {
    "q1": "large language models for information retrieval and ranking",
    "q2": "LLM for information retrieval and Ranking",
    "q3": "query Reformulation in information retrieval",
    "q4": "ranking Documents",
    "q5": "Optimizing recommendation systems with LLMs by leveraging item metadata"
}

# ============================================
# 8) RANKING POUR TOUTES LES QUERIES
# ============================================
print("\n=========== RANKING DES REQUÊTES (Produit TF) ===========")

for qname, qtext in queries.items():
    print(f"\n----- {qname} : {qtext} -----")
    ranking = rank_query_product(qtext, unigram_normalized)
    # afficher top 10 documents
    top10 = list(ranking.items())[:10]
    print(top10)
