# sections/token_viewer.py

import streamlit as st
import os

st.title("4. Sentences")

# Base directories for tokens
TOKEN_PATHS = {
    "Non-normalized": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Sentences\Raw",
    "Lancaster": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Sentences\Lancaster",
    "Porter": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Sentences\Porter",
    "Snowball": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Sentences\Snowball"
}

# --- First filter: choose normalization ---
normalization = st.radio(
    "Choose token type:",
    list(TOKEN_PATHS.keys())
)

BASE_DIR = TOKEN_PATHS[normalization]

# --- Second filter: article display options ---
option = st.radio(
    "Choose display mode:",
    ["Display all articles", "Display articles by volume", "Display a specific article"]
)

def display_sentences(file_path):
    """Read sentences and display them with <s> and </s> and a blank line in between."""
    with open(file_path, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]
    for sentence in sentences:
        st.write(f"[s] {sentence} [/s]")
        st.write("")  # blank line for spacing

# --- Display logic ---
if option == "Display all articles":
    for volume in sorted(os.listdir(BASE_DIR)):
        volume_path = os.path.join(BASE_DIR, volume)
        if not os.path.isdir(volume_path):
            continue
        st.header(volume)
        for file in sorted(os.listdir(volume_path), key=lambda x: int(x.split('_')[0])):
            file_path = os.path.join(volume_path, file)
            st.subheader(f"Article {file.replace('_S.txt','')}")
            display_sentences(file_path)

elif option == "Display articles by volume":
    volumes = [v for v in sorted(os.listdir(BASE_DIR)) if os.path.isdir(os.path.join(BASE_DIR, v))]
    selected_volume = st.selectbox("Select a volume:", volumes)

    if selected_volume:
        volume_path = os.path.join(BASE_DIR, selected_volume)
        st.header(selected_volume)
        for file in sorted(os.listdir(volume_path), key=lambda x: int(x.split('_')[0])):
            file_path = os.path.join(volume_path, file)
            st.subheader(f"Article {file.replace('_S.txt','')}")
            display_sentences(file_path)

elif option == "Display a specific article":
    volumes = [v for v in sorted(os.listdir(BASE_DIR)) if os.path.isdir(os.path.join(BASE_DIR, v))]
    selected_volume = st.selectbox("Select a volume:", volumes)

    if selected_volume:
        volume_path = os.path.join(BASE_DIR, selected_volume)
        articles = sorted(os.listdir(volume_path), key=lambda x: int(x.split('_')[0]))
        selected_article = st.selectbox("Select an article:", articles)

        if selected_article:
            file_path = os.path.join(volume_path, selected_article)
            st.header(f"{selected_volume} — Article {selected_article.replace('_S.txt','')}")
            display_sentences(file_path)
