import streamlit as st
import os
import itertools

st.title("7. Sentence Prediction with Bigrams")

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
# === Load bigrams ===
@st.cache(show_spinner=False, allow_output_mutation=True)
def load_bigrams(fp):
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
                if len(ngram) == 2:  # bigram only
                    ngram_probs[ngram] = float(proba)
            except Exception:
                continue
    return ngram_probs

bigrams = load_bigrams(file_path) if file_path else {}

if file_path:
    st.caption(f"Loaded from: `{file_path}`")
else:
    st.info("Please select a valid volume or article first.")

# === Bigram sentence prediction functions ===
def sentence_probability_bigram(tokens, bigram_probs):
    """Compute probability of a sequence of words using bigrams."""
    prob = 1.0
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i+1])
        p = bigram_probs.get(pair, 0)
        prob *= p
    return prob

def predict_sentence(tokens, bigram_probs, top_n=3):
    """Return top N permutations of tokens with non-zero probability."""
    if len(tokens) < 2:
        return [(tokens, 1.0)]
    
    all_perms = itertools.permutations(tokens)
    scored_perms = []

    for perm in all_perms:
        if any(w in ("<s>", "</s>") for w in perm):
            continue
        prob = sentence_probability_bigram(perm, bigram_probs)
        if prob > 0:  # only include non-zero probability
            scored_perms.append((perm, prob))

    return sorted(scored_perms, key=lambda x: x[1], reverse=True)[:top_n]

# === User input and prediction ===
user_input = st.text_input("Enter your words (any order):").strip().lower()

if user_input and bigrams:
    tokens = user_input.split()
    if len(tokens) < 2:
        st.warning("Enter at least two words for sentence prediction.")
    else:
        preds = predict_sentence(tokens, bigrams)
        if preds:
            st.write("Top predicted sentences:")
            for i, (perm, p) in enumerate(preds, start=1):
                st.write(f"{i}. {' '.join(perm)} (prob = {p:.6f})")
        else:
            st.info("No valid sentence could be generated (all permutations have probability 0).")
elif not file_path:
    st.info("Please select a valid volume or article first.")
