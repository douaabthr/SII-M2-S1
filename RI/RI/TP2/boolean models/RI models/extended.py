import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
import re
import ast

# ==================== PREPROCESSING ====================

query = "( query AND reformulation ) OR ( language AND model )"

query_spaced = query.replace('(', ' ( ').replace(')', ' ) ')

ExpReg = RegexpTokenizer(
    r'(?:[A-Za-z]\.)+'
    r'|[A-Za-z]+[\-@]\d+(?:\.\d+)?'
    r'|[\d#]+(?:[\.\,\-]\d+)*%?'
    r'|[A-Za-z]+'
)

tokens = []
for part in query_spaced.split():
    if part in ('(', ')'):
        tokens.append(part)
    else:
        tokens.extend(ExpReg.tokenize(part))

boolean_ops = {'and', 'or', 'not'}
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))

processed_tokens = []
for token in tokens:
    lower = token.lower()
    if lower in boolean_ops:
        processed_tokens.append(lower.upper())
    elif token in "()":
        processed_tokens.append(token)
    else:
        stemmed = porter.stem(lower)
        processed_tokens.append(stemmed)

processed_query = " ".join(processed_tokens)
print("Original query:", query)
print("Processed query:", processed_query)

# ==================== LOAD INDEX ====================

index = {}
with open("C:/Users/Imane/OneDrive/Bureau/ri/TP2/inverted_index_regex_porter.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 4:
            continue
        term, doc_id, _, weight = parts
        weight = float(weight)
        index.setdefault(term, {})[doc_id] = weight

all_docs = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6']

# ==================== EXTENDED BOOLEAN ====================

def RSV_AND(a, b):
    return   1 - (math.sqrt((1 - a)**2 + (1 - b)**2) / math.sqrt(2)) 

def RSV_OR(a, b):
    return math.sqrt(a**2 + b**2) / math.sqrt(2)

def RSV_NOT(a):
    return 1 - a


class ExtendedEvaluator(ast.NodeVisitor):
    def __init__(self, weights):
        self.weights = weights

    def visit_Name(self, node):
        return self.weights.get(node.id, 0.0)

    def visit_BoolOp(self, node):
        values = [self.visit(v) for v in node.values]
        if isinstance(node.op, ast.And):
            res = values[0]
            for v in values[1:]:
                res = RSV_AND(res, v)
            return res
        elif isinstance(node.op, ast.Or):
            res = values[0]
            for v in values[1:]:
                res = RSV_OR(res, v)
            return res
        else:
            raise ValueError("Unsupported boolean operator")

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.Not):
            return RSV_NOT(self.visit(node.operand))
        else:
            raise ValueError("Unsupported unary operator")

    def visit_Expr(self, node):
        return self.visit(node.value)


def prepare_query(query):
    expr = query.replace("AND", "and").replace("OR", "or").replace("NOT", "not")
    return expr


def eval_extended(query, doc_weights):
    expr = prepare_query(query)
    tree = ast.parse(expr, mode='eval')
    evaluator = ExtendedEvaluator(doc_weights)
    return evaluator.visit(tree.body)


terms = [t for t in processed_query.split() if t not in {"AND", "OR", "NOT", "(", ")"}]

extended_results = {}
for doc in all_docs:
    doc_weights = {term: index.get(term, {}).get(doc, 0.0) for term in terms}
    
    expr_display = processed_query
    for term, weight in doc_weights.items():
        expr_display = re.sub(rf"\b{re.escape(term)}\b", str(weight), expr_display)
    print(f"{doc}: {expr_display}")
    
    try:
        val = eval_extended(processed_query, doc_weights)
    except Exception as e:
        print(f"{doc} Eval error:", e)
        val = 0.0
    extended_results[doc] = val

# ==================== DISPLAY RESULTS ====================
print("\n===== Extended Boolean Model Results =====")
for doc, val in sorted(extended_results.items(), key=lambda x: x[1], reverse=True):
    print(f"{doc}: {val:.4f}")
