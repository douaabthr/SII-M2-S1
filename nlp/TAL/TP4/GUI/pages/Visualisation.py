import streamlit as st
import pandas as pd
import re

st.set_page_config(layout="wide")  # makes the layout wide

st.title("1. Visualisation")

# Path to CSV file
BASE_DIR = r"D:\study\nlp\TAL\TP4\article_labels\article_labels.csv"

# Load CSV
df = pd.read_csv(BASE_DIR)

# Extract numeric part from 'Article_Number'
df['Article_Number'] = df['Article_Number'].apply(lambda x: int(re.search(r'\d+', x).group()))

# Sort ascending by article number
df = df.sort_values(by='Article_Number', ascending=True).reset_index(drop=True)

# Display table without index, fill width manually
st.write(
    df[['Article_Number', 'Class_Label', 'Label_Name']].style.set_table_attributes('style="width:100%"')
)
