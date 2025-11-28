import streamlit as st
import pandas as pd
import os
import re

# -----------------------------------------
# Charger les attributs
# -----------------------------------------
def load_attributes(folder_path):
    attributes = {}
    for file in sorted(os.listdir(folder_path)):
        if file.startswith("."):
            continue
        att_name = file
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            patterns = sorted([line.strip() for line in f.readlines() if line.strip()])
            attributes[att_name] = patterns
    return attributes

# -----------------------------------------
# Compter occurrences exactes de séquences (regex)
# Multiplie par le nombre de mots
# -----------------------------------------
def count_attribute_frequency_regex(text, patterns):
    text_lower = text.lower()
    total = 0
    for pattern in patterns:
        pattern_lower = pattern.lower()
        n_words = len(pattern_lower.split())
        # Regex pour trouver la séquence comme mots entiers
        # \b = word boundary (début ou fin de mot)
        escaped_pattern = re.escape(pattern_lower)
        regex = r'\b' + escaped_pattern + r'\b'
        matches = re.findall(regex, text_lower)
        total += len(matches) * n_words if n_words > 1 else len(matches)
    return total

# -----------------------------------------
# Streamlit
# -----------------------------------------
st.title("Analyse automatique des attributs pour tous les articles")

attributes_dir = r"D:\study\nlp\TAL\TP6\Attributes\Attributes"
volumes_dir = r"D:\study\nlp\TAL\TP4\TP\All-in-many"

if os.path.isdir(attributes_dir) and os.path.isdir(volumes_dir):
    
    attributes = load_attributes(attributes_dir)
    st.success(f"{len(attributes)} attributs chargés.")

    article_files = sorted([f for f in os.listdir(volumes_dir) if not f.startswith(".")])
    n_articles = len(article_files)
    st.info(f"{n_articles} articles trouvés dans le dossier.")

    if n_articles == 0:
        st.warning("Aucun fichier trouvé dans le dossier.")
    else:
        data = []
        for idx, file in enumerate(article_files, start=1):
            article_path = os.path.join(volumes_dir, file)
            try:
                with open(article_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                st.warning(f"Impossible de lire le fichier {file}. Ignoré.")
                continue

            row = {"Article": file}

            for att, patterns in attributes.items():
                row[att] = count_attribute_frequency_regex(text, patterns)

            row["Label"] = ""
            data.append(row)

        df = pd.DataFrame(data)
        cols = ["Article"] + sorted([c for c in df.columns if c not in ["Article", "Label"]]) + ["Label"]
        df = df[cols]

        st.subheader("Tableau des fréquences")
        st.dataframe(df)

        st.download_button(
            "Télécharger tableau",
            df.to_csv(index=False).encode("utf-8"),
            "resultats_articles.csv",
            "text/csv"
        )

else:
    st.warning("⚠ Vérifiez les chemins des dossiers d'attributs ou des articles.")
