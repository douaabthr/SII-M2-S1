import streamlit as st
import pandas as pd
import os
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import LabelEncoder
import numpy as np

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
            pat_tokens = tokenize_text(pat)
            pat_norm = normalize_tokens(pat_tokens, norm_method)
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
        escaped_pattern = re.escape(pattern_lower)
        regex = r'(?<!-)\b' + escaped_pattern + r'\b(?!-)'
        matches = re.findall(regex, text_lower)
        total += len(matches) * (n_words if n_words > 1 else 1)
    return total

# -----------------------------------------
# Streamlit App
# -----------------------------------------
st.title("Analyse automatique des attributs et classification")

normalisation_choice = st.selectbox("Choisir méthode de normalisation :", ["Aucune", "Porter", "Lancaster", "Snowball"])

# Dossiers
attributes_dir = r"D:\study\nlp\TAL\TP6\Attributes\Attributes"
train_volumes_dir = r"D:\study\nlp\TAL\TP4\TP\All-in-many"
train_labels_dir = r"D:\study\nlp\TAL\TP4\TP\All-in-many_classification"
test_volumes_dir = r"D:\study\nlp\TAL\TP5\all-in-many_classification_testing"
test_labels_dir = r"D:\study\nlp\TAL\TP5\all-in-many_classification_testing"

if all(os.path.isdir(d) for d in [attributes_dir, train_volumes_dir, train_labels_dir, test_volumes_dir, test_labels_dir]):

    # ------------------------------ ENTRAINEMENT ------------------------------
    attributes = load_attributes_normalized(attributes_dir, normalisation_choice)
    st.success(f"{len(attributes)} attributs chargés.")
    
    train_files = sorted([f for f in os.listdir(train_volumes_dir) if not f.startswith(".")])
    n_train = len(train_files)
    st.info(f"{n_train} articles trouvés dans le dossier d'entraînement.")
    
    if n_train == 0:
        st.warning("Aucun fichier trouvé dans le dossier d'entraînement.")
    else:
        data = []
        labels_list = []
        
        for file in train_files:
            article_path = os.path.join(train_volumes_dir, file)
            label_path = os.path.join(train_labels_dir, file)
            
            try:
                with open(article_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                st.warning(f"Impossible de lire {file}. Ignoré.")
                continue
            
            try:
                with open(label_path, "r", encoding="utf-8") as f:
                    label = f.read().strip()
            except:
                label = ""
            
            if label == "":
                continue
            
            tokens = tokenize_text(text)
            norm_tokens = normalize_tokens(tokens, normalisation_choice)
            normalized_text = " ".join(norm_tokens)
            
            row = {"Article": file}
            for att, patterns in attributes.items():
                row[att] = count_attribute_frequency_regex(normalized_text, patterns)
            
            data.append(row)
            labels_list.append(label)
            print(data)
    

        df = pd.DataFrame(data)
        df["Label"] = labels_list
        cols = ["Article"] + sorted([c for c in df.columns if c not in ["Article","Label"]]) + ["Label"]
        df = df[cols]
        
        st.subheader("Tableau des fréquences")
        st.dataframe(df)
        
        st.download_button(
            "Télécharger tableau",
            df.to_csv(index=False).encode("utf-8"),
            "resultats_articles.csv",
            "text/csv"
        )
        
        # Préparation données PyTorch
        X = df.drop(columns=["Article","Label"]).values
        y = df["Label"].values
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y_encoded, dtype=torch.long)
        
        input_dim = X_tensor.shape[1]
        num_classes = len(le.classes_)
        
        # Modèle Logistic Regression

        class LogisticRegressionModel(nn.Module):
            def __init__(self, input_dim, num_classes):
                super().__init__()
                self.linear = nn.Linear(input_dim, num_classes)
                nn.init.zeros_(self.linear.weight)
                nn.init.zeros_(self.linear.bias)
            def forward(self, x):
                return self.linear(x)
        
        model = LogisticRegressionModel(input_dim, num_classes)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
        
        # Entraînement
# ------------------------------ Entraînement par batch ------------------------------
        epochs = 100
        batch_size = 64
        num_samples = X_tensor.shape[0]

        for epoch in range(epochs):
            for i in range(0, num_samples, batch_size):
                X_batch = X_tensor[i:i+batch_size]
                y_batch = y_tensor[i:i+batch_size]

                optimizer.zero_grad()
                outputs = model(X_batch)
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()

            if (epoch+1) % 10 == 0:
                st.write(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

        # Poids et softmax
        with torch.no_grad():
            outputs = model(X_tensor)
            probas = nn.Softmax(dim=1)(outputs).numpy()
            weights = model.linear.weight.detach().numpy()
        
        coef_matrix = pd.DataFrame(weights, columns=df.drop(columns=["Article","Label"]).columns)
        coef_matrix.index = le.classes_
        
        st.subheader("Matrice des poids par classe")
        st.dataframe(coef_matrix)
        # ------------------------------ Affichage du biais ------------------------------
        with torch.no_grad():
            bias = model.linear.bias.detach().numpy()  # Récupère le biais
            bias_df = pd.DataFrame(bias.reshape(1, -1), columns=le.classes_)
            
        st.subheader("Biais par classe")
        st.dataframe(bias_df)
# ------------------------------ Accuracy sur le train ------------------------------
        with torch.no_grad():
            outputs_train = model(X_tensor)
            predicted_indices = torch.argmax(outputs_train, dim=1)
            train_accuracy = (predicted_indices == y_tensor).float().mean().item()

        st.subheader(f"Accuracy sur le jeu d'entraînement : {train_accuracy*100:.2f}%")

        st.subheader("Exemple de probabilités softmax (5 premiers articles)")
        st.dataframe(pd.DataFrame(probas, columns=le.classes_).head())
        
        # ------------------------------ TEST SUR LE DOSSIER COMPLET ------------------------------
        st.subheader("Test sur le dossier de test complet")
        
        test_files = sorted([f for f in os.listdir(test_volumes_dir) if not f.startswith(".")])
        if len(test_files) == 0:
            st.warning("Aucun fichier trouvé dans le dossier de test.")
        else:
            y_true = []
            y_pred = []
            
            for file in test_files:
                article_path = os.path.join(test_volumes_dir, file)
                label_path = os.path.join(test_labels_dir, file)
                
                with open(article_path, "r", encoding="utf-8") as f:
                    text = f.read()
                with open(label_path, "r", encoding="utf-8") as f:
                    true_label = f.read().strip()
                
                tokens = tokenize_text(text)
                norm_tokens = normalize_tokens(tokens, normalisation_choice)
                normalized_text = " ".join(norm_tokens)
                
                x_test = [count_attribute_frequency_regex(normalized_text, patterns) for att, patterns in attributes.items()]
                x_test_tensor = torch.tensor([x_test], dtype=torch.float32)
                
                with torch.no_grad():
                    out = model(x_test_tensor)
                    pred_idx = torch.argmax(out, dim=1).item()
                    pred_label = le.inverse_transform([pred_idx])[0]
                
                y_true.append(true_label)
                y_pred.append(pred_label)
            
            accuracy = np.mean(np.array(y_true) == np.array(y_pred))
            st.write(f"Accuracy sur le dossier de test : **{accuracy*100:.2f}%**")
        
        # ------------------------------ TEST ARTICLE INDIVIDUEL ------------------------------
        st.subheader("Tester un article individuel du dossier de test")
        test_file_select = st.selectbox("Choisir un fichier de test :", test_files)
        
        if st.button("Tester cet article"):
            article_path = os.path.join(test_volumes_dir, test_file_select)
            label_path = os.path.join(test_labels_dir, test_file_select+"_label")
            
            with open(article_path, "r", encoding="utf-8") as f:
                text = f.read()
            with open(label_path, "r", encoding="utf-8") as f:
                true_label = f.read().strip()
            
            tokens = tokenize_text(text)
            norm_tokens = normalize_tokens(tokens, normalisation_choice)
            normalized_text = " ".join(norm_tokens)
            
            x_test = [count_attribute_frequency_regex(normalized_text, patterns) for att, patterns in attributes.items()]
            x_test_tensor = torch.tensor([x_test], dtype=torch.float32)
            
            with torch.no_grad():
                out = model(x_test_tensor)
                pred_idx = torch.argmax(out, dim=1).item()
                pred_label = le.inverse_transform([pred_idx])[0]
            
            st.write(f"Label réel : **{true_label}**")
            st.write(f"Label prédit : **{pred_label}**")
            acc = 1 if pred_label == true_label else 0
            st.write(f"Accuracy sur cet article : **{acc*100:.2f}%**")

else:
    st.warning("⚠ Vérifiez les chemins des dossiers d'attributs, d'entraînement et de test.")
