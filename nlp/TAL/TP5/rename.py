import os

folder = r"D:\study\nlp\TAL\TP5\All-in-many_classification_testing"

for filename in os.listdir(folder):
    full = os.path.join(folder, filename)

    if os.path.isfile(full) and not filename.endswith(".txt"):
        new_name = full + ".txt"
        os.rename(full, new_name)
        print(f"Renamed: {filename} → {filename}.txt")
