import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
#===============PREPROCESSING=================


query = "( query AND  reformulation) OR (Language  AND model)"

query_spaced = query.replace('(', ' ( ').replace(')', ' ) ')

ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'                    # Abbreviations like D.Z.A
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'       # Words combined with numbers, e.g., data-
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'          # Numbers with decimals, separators, or percentages
    r'|[A-Za-z]+'                         # Simple words (alphabetic)
)

tokens = []
for part in query_spaced.split():
    if part in ('(', ')'):  
        tokens.append(part)
    else:
        tokens.extend(ExpReg.tokenize(part))

# define what are boolean ops
boolean_ops = {'and', 'or', 'not'}
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))

processed_tokens = []

for token in tokens:
    lower_token = token.lower()
    if lower_token in boolean_ops:
        # keep operators as uppercase
        processed_tokens.append(lower_token.upper())
    elif token in "()":
        # keep parentheses as they are
        processed_tokens.append(token)

    # elif lower_token in stop_words:
    #     # skip stopords (logiquement they dont appear in docs)
    #     continue
    else:
        # apply preprocessing (stemming)
        stemmed = porter.stem(lower_token)
        processed_tokens.append(stemmed)

# rebuild query
processed_query = " ".join(processed_tokens)

print("Original query:", query)
print("Processed query:", processed_query)


#============LOADING INVERTED INDEX================
index = {}
with open("C:/Users/Imane/OneDrive/Bureau/ri/TP2/inverted_index_regex_porter.txt", "r", encoding="utf-8") as f:
    for line in f:
            parts = line.strip().split()
            term = parts[0]
            doc_id = parts[1]
            if term not in index:
                index[term] = set()
            index[term].add(doc_id)



# ================== PARSE AND EVALUATE QUERY ===================



terms = [t for t in processed_query.split() if t not in {"AND", "OR", "NOT", "(", ")"}]

satisfying_docs=set()

print("========Classical boolean=========")
all_docs=['D1','D2','D3','D4','D5','D6']
for doc in all_docs:
    # Build the boolean expression for this document
    expr = processed_query
    for term in terms:  # query terms
        val = "1" if doc in index.get(term, set()) else "0"
        expr = re.sub(rf"\b{re.escape(term)}\b", val, expr)

    # Replace operators with Python logical operators
    expr_bool = expr.replace("AND", " and ").replace("OR", " or ").replace("NOT", " not ")
    # Evaluate the boolean expression
    result = eval(expr_bool)

    # Print the expression and its value
    print(f"{doc}: {expr} -> {int(result)}")

    # Collect documents that satisfy the query
    if result:
        satisfying_docs.add(doc)

print("\nDocuments satisfying the query:", satisfying_docs)





#============== fuzzy boolean===============

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



import math

# =========== FUZZY BOOLEAN QUERY EVALUATION ===========

import ast 
print("\n========Fuzzy boolean=========")
# Fuzzy operators
def AND_(a, b): return min(a, b)
def OR_(a, b): return max(a, b)
def NOT_(a): return 1 - a

# Safe AST-based fuzzy evaluator
class FuzzyEvaluator(ast.NodeVisitor):
    def __init__(self, weights):
        self.weights = weights

    def visit_Name(self, node):
        # Replace term with its weight
        return self.weights.get(node.id, 0.0)

    def visit_BoolOp(self, node):
        values = [self.visit(v) for v in node.values]
        if isinstance(node.op, ast.And):
            return min(values)
        elif isinstance(node.op, ast.Or):
            return max(values)
        else:
            raise ValueError("Unsupported boolean operator")

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            return 1 - self.visit(node.operand)
        else:
            raise ValueError("Unsupported unary operator")

    def visit_Expr(self, node):
        return self.visit(node.value)

# Convert query to Python boolean expression
def prepare_query(query):
    expr = query
    expr = expr.replace("AND", "and").replace("OR", "or").replace("NOT", "not")
    return expr

# Evaluate fuzzy query for a document
def eval_fuzzy(query, doc_weights):
    expr = prepare_query(query)
    
    tree = ast.parse(expr, mode='eval')
    evaluator = FuzzyEvaluator(doc_weights)
    return evaluator.visit(tree.body)

# Get all query terms (excluding operators)
terms = [t for t in processed_query.split() if t not in {"AND", "OR", "NOT", "(", ")"}]

# Evaluate fuzzy query per document
fuzzy_results = {}
for doc in all_docs:
    doc_weights = {term: index.get(term, {}).get(doc, 0.0) for term in terms}
    
    # --- DEBUG: show query with weights replaced ---
    expr_display = processed_query
    for term, weight in doc_weights.items():
        expr_display = re.sub(rf"\b{re.escape(term)}\b", str(weight), expr_display)
    print(f"{doc}: {expr_display}")
    # --------------------------------------------------
    
    try:
        val = eval_fuzzy(processed_query, doc_weights)
    except Exception as e:
        print(f"{doc} Eval error:", e)
        val = 0.0
    fuzzy_results[doc] = val

# Sort and display
for doc, val in fuzzy_results.items():
    print(f"{doc}: {val}")