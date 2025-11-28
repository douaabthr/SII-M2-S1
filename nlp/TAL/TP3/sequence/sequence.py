import itertools
import math

# === LOAD BIGRAMS & TRIGRAMS ===
def load_ngrams(file_path):
    ngram_probs = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            ngram_str, freq, proba = parts
            ngram = eval(ngram_str)
            ngram_probs[ngram] = float(proba)
    return ngram_probs


# === SEQUENCE PROBABILITY USING BIGRAM MODEL ===
def sequence_probability(sequence, bigram_probs, smoothing=1e-8):
    log_prob = 0.0
    for i in range(1, len(sequence)):
        w_prev, w_curr = sequence[i-1], sequence[i]
        prob = bigram_probs.get((w_prev, w_curr), smoothing)
        log_prob += math.log(prob)
    return math.exp(log_prob)


# === MOST PROBABLE SEQUENCES ===
def find_top_sequences(words, bigram_probs, top_n=3):
    scored = []
    for perm in itertools.permutations(words):
        p = sequence_probability(perm, bigram_probs)
        scored.append((perm, p))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]


# === INTERPOLATED NEXT-WORD PREDICTION (0.4 BI + 0.6 TRI) ===
def predict_next_word(sequence, bigram_probs, trigram_probs, λ2=0.4, λ3=0.6):
    if len(sequence) < 2:
        return None, 0
    w1, w2 = sequence[-2], sequence[-1]
    candidates = {b[1] for b in bigram_probs if b[0] == w2}
    candidates |= {t[2] for t in trigram_probs if t[0] == w1 and t[1] == w2}

    best_word, best_score = None, 0
    for w3 in candidates:
        p_bi = bigram_probs.get((w2, w3), 0)
        p_tri = trigram_probs.get((w1, w2, w3), 0)
        score = λ2 * p_bi + λ3 * p_tri
        if score > best_score:
            best_score = score
            best_word = w3

    return best_word, best_score


# === FILE PATHS ===
bigram_file_path = r"D:\study\nlp\TAL\TP2\bigram\no normalization\per_volume\Volume 18_ngram.txt"
trigram_file_path = r"D:\study\nlp\TAL\TP2\trigram\no normalization\per_volume\Volume 18_ngram.txt"

# === LOAD DATA ===
bigrams = load_ngrams(bigram_file_path)
trigrams = load_ngrams(trigram_file_path)

# === USER INPUT ===
input_words = input("Enter words separated by spaces: ").strip().lower().split()

# === FIND TOP 3 SEQUENCES ===
top_sequences = find_top_sequences(input_words, bigrams, top_n=3)

# === DISPLAY RESULTS ===
print("\n=== Top 3 Most Probable Sequences (with Next Word Prediction) ===")
for seq, prob in top_sequences:
    next_word, score = predict_next_word(seq, bigrams, trigrams)
    seq_str = " ".join(seq)
    print(f" {seq_str:<30}{next_word} ")
