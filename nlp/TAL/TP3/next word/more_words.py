# sections/prediction_viewer.py

import streamlit as st
import os

# === PAGE TITLE ===
st.title("6. Next Word Prediction")

# === PATHS ===
BASE_BIGRAMS = r"D:\study\nlp\TAL\TP2\bigram"
BASE_TRIGRAMS = r"D:\study\nlp\TAL\TP2\trigram"

# === NORMALIZATION FILTER ===
normalization = st.radio(
    "Choose normalization:",
    ["no normalization", "Lancaster", "Porter", "Snowball"]
)

# === DOCUMENT FILTER ===
documents = ["all_articles", "vol1", "vol2", "vol3", "vol4", "vol5"]
selected_doc = st.selectbox("Choose document:", documents)

# === Construct paths ===
bigram_file_path = os.path.join(BASE_BIGRAMS, normalization, selected_doc, "all_articles_ngram.txt")
trigram_file_path = os.path.join(BASE_TRIGRAMS, normalization, selected_doc, "all_articles_ngram.txt")


# === LOAD N-GRAMS ===
@st.cache_data
def load_ngrams(file_path):
    ngram_probs = {}
    if not os.path.exists(file_path):
        st.warning(f"File not found: {file_path}")
        return ngram_probs
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            ngram_str, freq, proba = parts
            try:
                ngram = eval(ngram_str)  # convert string ('w1','w2',...) → tuple
                ngram_probs[ngram] = float(proba)
            except:
                continue
    return ngram_probs


# === PREDICTION FUNCTIONS ===
def predict_next_tokens_interpolated(tokens, bigram_probs, trigram_probs, λ3=0.6, λ2=0.4, top_n=3):
    """
    Interpolated prediction using bigrams and trigrams.
    """
    if len(tokens) == 0:
        return []

    # Single word → bigram only
    if len(tokens) == 1:
        w1 = tokens[-1]
        candidates = {b[1]: p for b, p in bigram_probs.items() if b[0] == w1}
        if not candidates:
            return []
        return sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Multi-word → interpolation
    w1, w2 = tokens[-2], tokens[-1]
    scores = {}

    possible_nexts = set([b[1] for b in bigram_probs if b[0] == w2])
    possible_nexts |= set([t[2] for t in trigram_probs if len(t) == 3 and t[0] == w1 and t[1] == w2])

    for next_word in possible_nexts:
        p2 = bigram_probs.get((w2, next_word), 0)
        p3 = trigram_probs.get((w1, w2, next_word), 0)
        scores[next_word] = λ3 * p3 + λ2 * p2

    if not scores:
        return []

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]


# === LOAD DATA ===
st.write("Loading n-grams ...")
bigrams = load_ngrams(bigram_file_path)
trigrams = load_ngrams(trigram_file_path)
st.success("N-grams loaded successfully!")

# === USER INPUT ===
input_text = st.text_input("Type one or more words:", "").strip().lower()

if input_text:
    tokens = input_text.split()
    top_predictions = predict_next_tokens_interpolated(tokens, bigrams, trigrams)

    if top_predictions:
        st.subheader("Top 3 Predictions:")
        for i, (word, prob) in enumerate(top_predictions, start=1):
            st.write(f"**{i}.** {word}  _(score = {prob:.6f})_")
    else:
        st.info(f"No predictions found for '{input_text}'.")
