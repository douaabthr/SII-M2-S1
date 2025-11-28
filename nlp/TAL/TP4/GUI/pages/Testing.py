import streamlit as st
import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer
from collections import Counter
from nltk.corpus import stopwords
import math
import os
from pathlib import Path
    
st.set_page_config(layout="wide")
st.title("3. Testing")

# -----------------------------
# INPUT: folder containing test files
# -----------------------------
st.subheader(" Choose folder containing your text files")
folder_path = st.text_input("Folder path:", 
                            r"D:\study\nlp\TAL\TP5\All-in-many_classification_testing")

folder_path = Path(folder_path)

# Initialize session_state for tokens
if "tokens" not in st.session_state:
    st.session_state.tokens = []

# Upload TXT file
uploaded_file = st.file_uploader("Choose a TXT file", type="txt")

# Preprocessing choice
filter_option = st.selectbox(
    "Choose normalisation method :",
    ["Snowball", "Porter", "Lancaster", "No Normalization"]
)

stop_words = set(stopwords.words('english'))

# -----------------------------
# PREPROCESSING
# -----------------------------
if uploaded_file:
    text = uploaded_file.read().decode("utf-8")

    if st.button("Pre-process"):
        # Tokenize
        pattern = r'(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[.,\-]\d+)?%?|\w+(?:[-/]\w+)*|[.!?]+'
        tokenizer = nltk.RegexpTokenizer(pattern)
        tokens = tokenizer.tokenize(text)
        tokens = [t for t in tokens if t.lower() not in stop_words]

        # Normalization
        if filter_option == "Porter":
            stemmer = PorterStemmer()
            tokens = [stemmer.stem(t) for t in tokens]
        elif filter_option == "Snowball":
            stemmer = SnowballStemmer("english")
            tokens = [stemmer.stem(t) for t in tokens]
        elif filter_option == "Lancaster":
            stemmer = LancasterStemmer()
            tokens = [stemmer.stem(t) for t in tokens]

        st.session_state.tokens = tokens
        st.subheader("Tokens:")
        st.write(" ".join(tokens))


# -----------------------------
# CLASSIFICATION
# -----------------------------
if uploaded_file and st.session_state.tokens:
    if st.button("Test / Classify"):
        
        tokens = st.session_state.tokens

        # Load probability CSVs
        BASE_DIR = r"D:\study\nlp\TAL\TP4\term_probabilities"
        file_map = {
            "No Normalization": f"{BASE_DIR}\\word_probs_Original.csv",
            "Porter": f"{BASE_DIR}\\word_probs_Porter.csv",
            "Snowball": f"{BASE_DIR}\\word_probs_Snowball.csv",
            "Lancaster": f"{BASE_DIR}\\word_probs_Lancaster.csv"
        }
        df_probs = pd.read_csv(file_map[filter_option])

        # Label mapping
        LABEL_MAP = {
            "1": "Metaheuristics",
            "2": "Machine & Deep Learning",
            "3": "Combination of Metaheuristics & Machine/Deep Learning",
            "4": "Others"
        }
        REVERSE_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

        # Rename columns
        new_cols = {}
        for col in df_probs.columns:
            if col.startswith("P(class"):
                num = re.findall(r'\d+', col)[0]
                if num in LABEL_MAP:
                    new_cols[col] = LABEL_MAP[num]
        df_probs = df_probs.rename(columns=new_cols)

        class_cols = [c for c in df_probs.columns if c in LABEL_MAP.values()]

        # LOG PROBABILITIES
        class_probs = {c: 0.0 for c in class_cols}
        unknown_tokens = []
        term_table_rows = []

        # Load class priors
        class_prior_csv = r"D:\study\nlp\TAL\TP4\class_probabilities\class_probabilities.csv"
        df_class = pd.read_csv(class_prior_csv)
        class_priors = {row["Label_Name"]: row["P(c)"] for _, row in df_class.iterrows()}

        # Compute token contributions
        token_counts = Counter(tokens)
        for token, count in token_counts.items():
            row = df_probs[df_probs["Term"] == token]
            if not row.empty:
                term_probs = {"Term": token}
                for c in class_cols:
                    p = row.iloc[0][c]
                    term_probs[c] = p
                    if p > 0:
                        class_probs[c] += count * math.log10(p)
                term_table_rows.append(term_probs)
            else:
                unknown_tokens.append(token)

        # Add priors
        for c in class_probs:
            if c in class_priors:
                class_probs[c] += math.log10(class_priors[c])

        # Sort results
        sorted_probs = sorted(class_probs.items(), key=lambda x: x[1], reverse=True)
        pred_name = sorted_probs[0][0]
        pred_num = REVERSE_LABEL_MAP[pred_name]

        # Display prediction
        st.subheader(f"Predicted Class: **{pred_num} – {pred_name}**")

        # -----------------------------
        # EXPECTED CLASS (GROUND TRUTH)
        # -----------------------------
        

        uploaded_filename = uploaded_file.name
        name, ext = uploaded_filename.rsplit(".", 1)
        expected_filename = f"{name}_label.{ext}"
        expected_path = folder_path / expected_filename

        if expected_path.exists():
            with open(expected_path, "r", encoding="utf-8") as f:
                expected = f.read().strip()

            st.subheader(f"Expected Class: {expected}")
        else:
            st.info(f"No expected file found: {expected_filename}")


        # -----------------------------
        # RESULT TABLE
        # -----------------------------
        df_result = pd.DataFrame({
            "Class Number": [REVERSE_LABEL_MAP[c] for c, _ in sorted_probs],
            "Class Name": [c for c, _ in sorted_probs],
            "Log(Probability)": [round(p, 10) for _, p in sorted_probs]
        })
        st.write(df_result)

        # Unknown tokens
        if unknown_tokens:
            st.subheader("Unknown Tokens:")
            st.write(" ".join(unknown_tokens))

        # Term probabilities
        if term_table_rows:
            st.subheader("Term Probabilities per Class:")
            df_terms = pd.DataFrame(term_table_rows)
            df_terms = df_terms[["Term"] + class_cols]
            st.write(df_terms)


