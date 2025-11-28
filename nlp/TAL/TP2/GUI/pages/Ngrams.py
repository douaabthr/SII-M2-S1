# sections/ngram_viewer.py
import streamlit as st
import os
import pandas as pd
import ast  # to safely parse tuple-like strings

st.title("5. N-grams")

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

ngram_type = st.radio(
    "Choose N-gram type:",
    ["unigram", "bigram", "trigram"]
)

# Determine base directory depending on normalization
if normalization == "no normalization":
    BASE_DIR = os.path.join(BASE_NGRAMS, ngram_type, "no normalization")
else:
    BASE_DIR = os.path.join(BASE_NGRAMS, ngram_type, "normalization", normalization)


# === HELPERS ===
def parse_ngram(value):
    """
    Convert tuple-like strings such as "('of', 'the')" into "of the".
    Keep normal strings as they are.
    """
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, tuple):
            return " ".join(parsed)
        return str(parsed)
    except Exception:
        return value


def load_ngram_file(file_path):
    """
    Load ngram file and return a DataFrame with columns: Ngram, Frequency, Probability.
    """
    df = pd.read_csv(file_path, sep="\t", header=None, names=["N-gram", "Frequency", "Probability"], quoting=3)
    # Convert tuple-like strings to words
    df["N-gram"] = df["N-gram"].apply(parse_ngram)
    return df


# --- Collect all n-grams ---
all_dfs = []

# --- MAIN LOGIC ---
if option == "All articles":
    all_dir = os.path.join(BASE_DIR, "all_articles")
    all_file = os.path.join(all_dir, "all_articles_ngram.txt")
    if os.path.exists(all_file):
        st.info(f"Loading file: {all_file}")
        df = load_ngram_file(all_file)
        all_dfs.append(df)
    else:
        st.warning(f"No file found: {all_file}")

elif option == "By volume":
    per_volume_dir = os.path.join(BASE_DIR, "per_volume")
    if not os.path.exists(per_volume_dir):
        st.warning("No per-volume directory found.")
    else:
        volumes = [f.replace("_ngram.txt", "") for f in sorted(os.listdir(per_volume_dir)) if f.endswith("_ngram.txt")]
        selected_volume = st.selectbox("Select a volume:", volumes)
        if selected_volume:
            volume_file = os.path.join(per_volume_dir, f"{selected_volume}_ngram.txt")
            if os.path.exists(volume_file):
                st.info(f"Loading file: {volume_file}")
                df = load_ngram_file(volume_file)
                all_dfs.append(df)
            else:
                st.warning(f"No file found: {volume_file}")

elif option == "Specific article":
    per_article_dir = os.path.join(BASE_DIR, "per_article")
    if not os.path.exists(per_article_dir):
        st.warning("No per-article directory found.")
    else:
        volumes = [v for v in sorted(os.listdir(per_article_dir)) if os.path.isdir(os.path.join(per_article_dir, v))]
        selected_volume = st.selectbox("Select a volume:", volumes)
        if selected_volume:
            volume_path = os.path.join(per_article_dir, selected_volume)
            articles = sorted(os.listdir(volume_path), key=lambda x: int(x.split('_')[0]))
            selected_article = st.selectbox("Select an article:", articles)
            if selected_article:
                file_path = os.path.join(volume_path, selected_article)
                if os.path.exists(file_path):
                    st.info(f"Loading file: {file_path}")
                    df = load_ngram_file(file_path)
                    all_dfs.append(df)
                else:
                    st.warning(f"No file found: {file_path}")

# --- Combine and display ---
if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)

    # --- Add search box ---
    search_term = st.text_input("🔍 Search n-grams:")
    if search_term:
        combined = combined[combined["N-gram"].str.contains(search_term, case=False, na=False)]

    # --- Display table ---
    st.dataframe(combined, width=1200, height=600)

    st.markdown("---")
    total_ngrams = combined["Frequency"].sum()
    unique_ngrams = combined["N-gram"].nunique()
    st.write(f"**Total {ngram_type.lower()}s:** {total_ngrams}")
    st.write(f"**Unique {ngram_type.lower()}s:** {unique_ngrams}")

else:
    st.warning("No n-grams to display. Please check your files or selection.")
