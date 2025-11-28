import streamlit as st
import os

st.title("6. Next Word Prediction")

# === BASE PATHS ===
BASE_NGRAMS = r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2"

# --- Filters ---
normalization = st.radio(
    "Choose normalization:",
    ["no normalization", "Lancaster", "Porter", "Snowball"]
)

option = st.radio(
    "Choose article display mode:",
    ["All articles", "By volume", "Specific article"]
)

# Input mode filter
input_mode = st.radio("Prediction type:", ["One word", "At least two words"])

# Determine base directory
if normalization == "no normalization":
    BASE_DIR = os.path.join(BASE_NGRAMS, "bigram", "no normalization")
else:
    BASE_DIR = os.path.join(BASE_NGRAMS, "bigram", "normalization", normalization)

# === Select file_path based on folder structure ===
file_path = None

if option == "All articles":
    candidate_file = os.path.join(BASE_DIR, "all_articles", "all_articles_ngram.txt")
    if os.path.exists(candidate_file):
        file_path = candidate_file
    else:
        st.warning(f"No file found: {candidate_file}")

elif option == "By volume":
    per_volume_dir = os.path.join(BASE_DIR, "per_volume")
    if os.path.exists(per_volume_dir):
        volumes = [f.replace("_ngram.txt", "") for f in sorted(os.listdir(per_volume_dir)) if f.endswith("_ngram.txt")]
        if volumes:
            selected_volume = st.selectbox("Select a volume:", volumes)
            candidate_file = os.path.join(per_volume_dir, f"{selected_volume}_ngram.txt")
            if os.path.exists(candidate_file):
                file_path = candidate_file
            else:
                st.warning(f"No file found: {candidate_file}")
    else:
        st.warning("No per-volume directory found.")

elif option == "Specific article":
    per_article_dir = os.path.join(BASE_DIR, "per_article")
    if os.path.exists(per_article_dir):
        volumes = [v for v in sorted(os.listdir(per_article_dir)) if os.path.isdir(os.path.join(per_article_dir, v))]
        if volumes:
            selected_volume = st.selectbox("Select a volume:", volumes)
            volume_path = os.path.join(per_article_dir, selected_volume)
            articles = sorted(os.listdir(volume_path), key=lambda x: int(x.split('_')[0]))
            if articles:
                selected_article = st.selectbox("Select an article:", articles)
                candidate_file = os.path.join(volume_path, selected_article)
                if os.path.exists(candidate_file):
                    file_path = candidate_file
                else:
                    st.warning(f"No file found: {candidate_file}")
    else:
        st.warning("No per-article directory found.")

# === Load ngrams ===
@st.cache(show_spinner=False, allow_output_mutation=True)
def load_ngrams(fp):
    ngram_probs = {}
    if not os.path.exists(fp):
        return ngram_probs
    with open(fp, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            ngram_str, freq, proba = parts
            try:
                ngram = eval(ngram_str)
                ngram_probs[ngram] = float(proba)
            except Exception:
                continue
    return ngram_probs

@st.cache(show_spinner=False, allow_output_mutation=True)
def load_all_ngrams(fp):
    bigrams = load_ngrams(fp)
    trigram_file = fp.replace("bigram", "trigram")
    trigrams = load_ngrams(trigram_file)
    return bigrams, trigrams

if file_path:
    bigrams, trigrams = load_all_ngrams(file_path)
    st.caption(f"Loaded from: `{file_path}`")
else:
    bigrams, trigrams = {}, {}

# === Prediction functions ===
def predict_bigram(word, bigram_probs, top_n=3):
    candidates = {b[1]: p for b, p in bigram_probs.items() if b[0] == word}
    return sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:top_n]

def predict_interpolated(tokens, bigram_probs, trigram_probs, λ3=0.6, λ2=0.4, top_n=3):
    if len(tokens) < 2:
        return []
    w1, w2 = tokens[-2], tokens[-1]
    scores = {}
    possible_nexts = set([b[1] for b in bigram_probs if b[0] == w2])
    possible_nexts |= set([t[2] for t in trigram_probs if t[0] == w1 and t[1] == w2])
    for next_word in possible_nexts:
        p2 = bigram_probs.get((w2, next_word), 0)
        p3 = trigram_probs.get((w1, w2, next_word), 0)
        scores[next_word] = λ3 * p3 + λ2 * p2
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

# === User input and predictions ===
user_input = st.text_input("Enter your word(s):").strip().lower()

if user_input and file_path:
    tokens = user_input.split()
    if input_mode == "One word":
        if len(tokens) != 1:
            st.warning("Please enter exactly one word.")
        else:
            preds = predict_bigram(tokens[0], bigrams)
            if preds:
                
                for i, (w, p) in enumerate(preds, start=1):
                    st.write(f"{i}. **{w}** (prob = {p:.6f})")
            else:
                st.info("No prediction found.")
    else:
        if len(tokens) < 2:
            st.warning("Enter at least two words.")
        else:
            preds = predict_interpolated(tokens, bigrams, trigrams)
            if preds:
                
                for i, (w, p) in enumerate(preds, start=1):
                    st.write(f"{i}. **{w}** (score = {p:.6f})")
            else:
                st.info("No prediction found.")
elif not file_path:
    st.info("Please select a valid volume or article first.")
