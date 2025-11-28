import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="wide")  # makes the layout wide

st.title("2. Training")

st.subheader("Estimating class probabilities P(C)")
# Path to CSV file
BASE_DIR = r"D:\study\nlp\TAL\TP4\class_probabilities\class_probabilities.csv"

# Load CSV
df = pd.read_csv(BASE_DIR)



# Display table without index, fill width manually
st.write(
    df[['Class_Label', 'Label_Name', 'Document_Count', 'P(c)']]
    .style
    .hide(axis="index")  # ✅ removes index column
    .set_table_attributes('style="width:100%"')
)



st.subheader("Estimating conditional probabilities P(w|C)")

BASE_DIR = r"D:\study\nlp\TAL\TP4\term_probabilities"
files = {
   
    "Snowball Stemmer": f"{BASE_DIR}\\word_probs_Snowball.csv",
    "Porter ": f"{BASE_DIR}\\word_probs_Porter.csv" ,
    "Lancaster": f"{BASE_DIR}\\word_probs_Lancaster.csv" ,
     "No normalization": f"{BASE_DIR}\\word_probs_Original.csv"

}

# ---- Dropdown for normalization choice ----
option = st.selectbox(
    "Choose normalisation method :",
    list(files.keys())
)

# ---- Load the selected CSV ----
df = pd.read_csv(files[option])
LABEL_MAP = {
    "1": "Metaheuristics",
    "2": "Machine & Deep Learning",
    "3": "Combination of Metaheuristics & Machine/Deep Learning",
    "4": "Others"
}
new_columns = {}
for col in df.columns:
    if col.startswith("P(class"):
        class_num = col[-2] if col[-2].isdigit() else col[-1]  # handles 1-digit class numbers
        if class_num in LABEL_MAP:
            new_columns[col] = f"P({LABEL_MAP[class_num]})"

df = df.rename(columns=new_columns)
# ---- Search bar ----
search = st.text_input("🔍 Search", "")

# Filter dataframe based on search input
if search:
    df_filtered = df[df['Term'].astype(str).str.contains(search, case=False, na=False)]
else:
    df_filtered = df

# ---- Display ----

st.write(
    df_filtered.style
    .hide(axis="index")  # hide index column
    .set_table_attributes('style="width:100%"')
)