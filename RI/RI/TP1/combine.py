import nltk
from nltk.tokenize import RegexpTokenizer 
from nltk.stem import PorterStemmer,LancasterStemmer
import os
from collections import Counter
import math



# Tokenizer to extract digits from filenames (works like regex)
num_tokenizer = RegexpTokenizer(r'\d+')

base_folder = "C:/Users/Imane/OneDrive/Bureau/ri/TP1/Terms"

porter_folders = [
    "Terms_split_porter",
    "Terms_regex_porter"
]

for folder_name in porter_folders:
    folder_path = os.path.join(base_folder, folder_name)
    output_path = os.path.join(folder_path, f"combined_{folder_name}.txt")

    # Get all text files
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    # Sort by document number (extract digits using NLTK tokenizer)
    def extract_num(filename):
        tokens = num_tokenizer.tokenize(filename)
        return int(tokens[0]) if tokens else float('inf')

    txt_files.sort(key=extract_num)

    print(f"\nCombining {len(txt_files)} files in: {folder_name}")

    with open(output_path, "w", encoding="utf-8") as outfile:
        for filename in txt_files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                contents = infile.read()
                outfile.write(contents)
                outfile.write("\n")  # optional separator

    print(f"✅ Combined file saved at: {output_path}")

