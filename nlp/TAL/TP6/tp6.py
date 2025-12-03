import streamlit as st
import pandas as pd
import os
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer

# -----------------------------------------
# Télécharger ressources NLTK
# -----------------------------------------
nltk.download("punkt")

# -----------------------------------------
# Initialiser les stemmers
# -----------------------------------------
porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = SnowballStemmer("english")

# -----------------------------------------
# Fonction de normalisation
# -----------------------------------------
def normalize_tokens(tokens, method):
    if method == "Aucune":
        return [t.lower() for t in tokens]

    if method == "Porter":
        return [porter.stem(t.lower()) for t in tokens]

    if method == "Lancaster":
        return [lancaster.stem(t.lower()) for t in tokens]

    if method == "Snowball":
        return [snowball.stem(t.lower()) for t in tokens]

    return tokens


# -----------------------------------------
# Tokenizer personnalisé
# -----------------------------------------
ExpReg = nltk.RegexpTokenizer(r'<\/?s>|(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[.,\-]\d+)?%?|\w+(?:[-/]\w+)*|[.!?]+')


def tokenize_text(text):
    return ExpReg.tokenize(text)


# -----------------------------------------
# Charger les attributs
# -----------------------------------------
def load_attributes_normalized(folder_path, norm_method):
    attributes = {}
    for file in sorted(os.listdir(folder_path)):
        if file.startswith("."):
            continue

        file_path = os.path.join(folder_path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        normalized_patterns = []

        for pat in lines:
            # Tokeniser le pattern
            pat_tokens = tokenize_text(pat)

            # Normaliser le pattern
            pat_norm = normalize_tokens(pat_tokens, norm_method)

            # Reformater pour regex (ex: ["machine","learn"] → "machine learn")
            normalized_patterns.append(" ".join(pat_norm))

        attributes[file] = normalized_patterns

    return attributes


# -----------------------------------------
# Compter occurrences exactes de séquences (regex)
# -----------------------------------------
def count_attribute_frequency_regex(text, patterns):
    text_lower = text.lower()
    total = 0

    for pattern in patterns:
        pattern_lower = pattern.lower()

        n_words = len(pattern_lower.split())

        # Échapper les caractères spéciaux
        escaped_pattern = re.escape(pattern_lower)

        # Empêcher les matches avec "optimisation-base"
        regex = (
            r'(?<!-)\b'        # limite gauche mais pas après un tiret
            + escaped_pattern +
            r'\b(?!-)'         # limite droite mais pas avant un tiret
        )

        matches = re.findall(regex, text_lower)

        # pondération multi-mots
        total += len(matches) * (n_words if n_words > 1 else 1)

    return total

# -----------------------------------------
# Streamlit App
# -----------------------------------------
st.title("Analyse automatique des attributs pour tous les articles")

# Choix méthode de normalisation
normalisation_choice = st.selectbox(
    "Choisir méthode de normalisation :",
    ["Aucune", "Porter", "Lancaster", "Snowball"]
)

attributes_dir = r"D:\study\nlp\TAL\TP6\Attributes\Attributes"
volumes_dir = r"D:\study\nlp\TAL\TP4\TP\All-in-many"

if os.path.isdir(attributes_dir) and os.path.isdir(volumes_dir):
    
    attributes = load_attributes_normalized(attributes_dir, normalisation_choice)
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

            # Tokenisation
            tokens = tokenize_text(text)

            # Normalisation en fonction du choix utilisateur
            norm_tokens = normalize_tokens(tokens, normalisation_choice)

            # Re-créer le texte normalisé pour la regex
            normalized_text = " ".join(norm_tokens)

            row = {"Article": file}

            for att, patterns in attributes.items():
                row[att] = count_attribute_frequency_regex(normalized_text, patterns)

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
