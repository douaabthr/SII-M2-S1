# sections/article_viewer.py

import streamlit as st
import os


st.title("1. Articles")
BASE_DIR = "D:/study/nlp/TAL/TP2/text extraction"



# Main page options
option = st.radio(
    "Choose an option:",
    ["Display all articles", "Display articles by volume", "Display a specific article"]
)

# Display logic
if option == "Display all articles":
    for volume in sorted(os.listdir(BASE_DIR)):
        volume_path = os.path.join(BASE_DIR, volume)
        if not os.path.isdir(volume_path):
            continue
        st.header(volume)
        for file in sorted(os.listdir(volume_path), key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(volume_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.subheader(f"Article {file.replace('.txt','')}")
            st.write(content)

elif option == "Display articles by volume":
    volumes = [v for v in sorted(os.listdir(BASE_DIR)) if os.path.isdir(os.path.join(BASE_DIR, v))]
    selected_volume = st.selectbox("Select a volume:", volumes)

    if selected_volume:
        volume_path = os.path.join(BASE_DIR, selected_volume)
        st.header(selected_volume)
        for file in sorted(os.listdir(volume_path), key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(volume_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.subheader(f"Article {file.replace('.txt','')}")
            st.write(content)

elif option == "Display a specific article":
    volumes = [v for v in sorted(os.listdir(BASE_DIR)) if os.path.isdir(os.path.join(BASE_DIR, v))]
    selected_volume = st.selectbox("Select a volume:", volumes)

    if selected_volume:
        volume_path = os.path.join(BASE_DIR, selected_volume)
        articles = sorted(os.listdir(volume_path), key=lambda x: int(x.split('.')[0]))
        selected_article = st.selectbox("Select an article:", articles)

        if selected_article:
            file_path = os.path.join(volume_path, selected_article)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            st.header(f"{selected_volume} — Article {selected_article.replace('.txt','')}")
            st.write(content)
