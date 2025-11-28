import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# === Load the tokens ===
with open("TP1/exo1/text preprocessing/T.txt", "r", encoding="utf-8") as f:
    tokens = f.read()

with open("TP1/exo1/text preprocessing/T_N.txt", "r", encoding="utf-8") as f:
    normalized_tokens = f.read()

# === Generate word clouds ===
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tokens)
wordcloud2 = WordCloud(width=800, height=400, background_color='white').generate(normalized_tokens)

# === Display both side by side ===
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# First word cloud
axes[0].imshow(wordcloud, interpolation='bilinear')
axes[0].set_title("Original Tokens", fontsize=16)
axes[0].axis('off')

# Second word cloud
axes[1].imshow(wordcloud2, interpolation='bilinear')
axes[1].set_title("Normalized Tokens", fontsize=16)
axes[1].axis('off')

plt.tight_layout()
plt.show()
