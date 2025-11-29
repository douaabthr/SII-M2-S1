# Read the original file
input_file = r"C:\Users\Imane\OneDrive\Bureau\ri\TP4\inverted_index_regex_porter.txt"
output_file = r"C:\Users\Imane\OneDrive\Bureau\ri\TP4\vocab.txt"

unique_terms = set()

with open(input_file, "r") as f:
    for line in f:
        first_term = line.split()[0]  # get the first term
        unique_terms.add(first_term)

# Save unique terms to a new file
with open(output_file, "w") as f:
    for term in sorted(unique_terms):
        f.write(term + "\n")

print(f"Unique first terms saved to {output_file}")