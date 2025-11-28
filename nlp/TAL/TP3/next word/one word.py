def load_bigrams(file_path):
    bigram_probs = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            bigram_str, freq, proba = parts
            # Convert string representation ('word1', 'word2') into a tuple
            bigram = eval(bigram_str)
            bigram_probs[bigram] = float(proba)
    return bigram_probs


def predict_top_tokens(current_token, bigram_probs, top_n=5):
    # Filter all bigrams starting with the current token
    candidates = {b[1]: p for b, p in bigram_probs.items() if b[0] == current_token}
    if not candidates:
        return []
    # Sort by probability (descending)
    sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
    print("Number of candidates:", len(candidates))
    return sorted_candidates[:top_n]


# === Example usage ===
file_path = r"D:\study\nlp\TAL\TP2\bigram\no normalization\all_articles\all_articles_ngram.txt"
bigrams = load_bigrams(file_path)

token = input("Enter a token: ").strip().lower()  # read user input
top_tokens = predict_top_tokens(token, bigrams, top_n=5)

if top_tokens:
    print(f"\nTop 3 :")
    for i, (tok, prob) in enumerate(top_tokens, start=1):
        print(f"{i}. {tok}  (prob = {prob:.5f})")
else:
    print(f"No predictions found for '{token}'.")
