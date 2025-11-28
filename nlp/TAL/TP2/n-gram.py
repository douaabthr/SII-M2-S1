import os
from collections import Counter

# Input paths
tokens_dir = r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Tokens"
normalized_dirs = {
    "porter": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Porter\Normalized_Tokens",
    "lancaster": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Lancaster\Normalized_Tokens",
    "snowball": r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2\text preprocessing\Snowball\Normalized_Tokens",
}

# Output base
base_out = r"C:\Users\Imane\OneDrive\Bureau\TAL\TP2"

# Function to compute n-grams
def compute_ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def extract_number(filename):
    return int(filename.split('_')[0])

# Generic function to compute frequencies and probabilities
def compute_freq_prob(tokens, n):
    ngrams = compute_ngrams(tokens, n)
    freq_counter = Counter(ngrams)
    if n == 1:
        total = len(tokens)
        prob_counter = {gram: freq/total for gram, freq in freq_counter.items()}
    else:
        prev_ngrams = compute_ngrams(tokens, n-1)
        prev_counter = Counter(prev_ngrams)
        prob_counter = {gram: freq/prev_counter[gram[:-1]] for gram, freq in freq_counter.items()}
    return freq_counter, prob_counter

# Function to save n-grams to file
def save_ngrams(counter_freq, counter_prob, out_file):
    with open(out_file, "w", encoding="utf-8") as f:
        for gram, freq in counter_freq.items():
            proba = counter_prob[gram]
            f.write(f"{gram}\t{freq}\t{proba:.6f}\n")

# Function to process per article (current behavior)
def process_per_article(volume_path, output_dir, n):
    os.makedirs(output_dir, exist_ok=True)
    files = sorted(os.listdir(volume_path), key=extract_number)
    for file in files:
        file_path = os.path.join(volume_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            tokens = f.read().split()
        freq_counter, prob_counter = compute_freq_prob(tokens, n)
        save_ngrams(freq_counter, prob_counter, os.path.join(output_dir, f"{file.split('.')[0]}_ngram.txt"))

# Function to process per volume (aggregate all articles)
def process_per_volume(volume_path, output_dir, n):
    os.makedirs(output_dir, exist_ok=True)
    all_tokens = []
    files = sorted(os.listdir(volume_path), key=extract_number)
    for file in files:
        file_path = os.path.join(volume_path, file)
        with open(file_path, "r", encoding="utf-8") as f:
            all_tokens.extend(f.read().split())
    freq_counter, prob_counter = compute_freq_prob(all_tokens, n)
    out_file = os.path.join(output_dir, f"{os.path.basename(volume_path)}_ngram.txt")
    save_ngrams(freq_counter, prob_counter, out_file)

# Function to process all articles (aggregate everything)
def process_all_articles(base_dir, output_dir, n):
    os.makedirs(output_dir, exist_ok=True)
    all_tokens = []
    for volume in os.listdir(base_dir):
        volume_path = os.path.join(base_dir, volume)
        if not os.path.isdir(volume_path):
            continue
        for file in os.listdir(volume_path):
            file_path = os.path.join(volume_path, file)
            with open(file_path, "r", encoding="utf-8") as f:
                all_tokens.extend(f.read().split())
    freq_counter, prob_counter = compute_freq_prob(all_tokens, n)
    out_file = os.path.join(output_dir, f"all_articles_ngram.txt")
    save_ngrams(freq_counter, prob_counter, out_file)

# --- Process all n-grams ---
for n, ngram_name in zip([1,2,3], ["unigram", "bigram", "trigram"]):

    # No normalization
    no_norm_dir = os.path.join(base_out, ngram_name, "no normalization")

    # Per article
    for volume in os.listdir(tokens_dir):
        volume_path = os.path.join(tokens_dir, volume)
        if not os.path.isdir(volume_path):
            continue
        process_per_article(volume_path, os.path.join(no_norm_dir, "per_article", volume), n)

    # Per volume
    for volume in os.listdir(tokens_dir):
        volume_path = os.path.join(tokens_dir, volume)
        if not os.path.isdir(volume_path):
            continue
        process_per_volume(volume_path, os.path.join(no_norm_dir, "per_volume"), n)

    # All articles
    process_all_articles(tokens_dir, os.path.join(no_norm_dir, "all_articles"), n)

    # Normalized
    norm_base = os.path.join(base_out, ngram_name, "normalization")
    for stemmer, stem_dir in normalized_dirs.items():
        # Per article
        for volume in os.listdir(stem_dir):
            volume_path = os.path.join(stem_dir, volume)
            if not os.path.isdir(volume_path):
                continue
            process_per_article(volume_path, os.path.join(norm_base, stemmer, "per_article", volume), n)
        # Per volume
        for volume in os.listdir(stem_dir):
            volume_path = os.path.join(stem_dir, volume)
            if not os.path.isdir(volume_path):
                continue
            process_per_volume(volume_path, os.path.join(norm_base, stemmer, "per_volume"), n)
        # All articles
        process_all_articles(stem_dir, os.path.join(norm_base, stemmer, "all_articles"), n)
