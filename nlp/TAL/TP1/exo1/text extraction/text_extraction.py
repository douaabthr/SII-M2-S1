from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

myurl = "https://link.springer.com/journal/12065/volumes-and-issues/18-5"
html = urlopen(myurl).read()
soup = BeautifulSoup(html, "html.parser")

h3_tags = soup.find_all("h3", {"class": "app-card-open__heading"})

articles = []

for h3_tag in h3_tags:
    title = h3_tag.get_text(strip=True)
    article_link = "https://link.springer.com" + h3_tag.find('a')['href']

    article_html = urlopen(article_link).read()
    article_soup = BeautifulSoup(article_html, "html.parser")

    abstract_tag = article_soup.find("div", {"class": "c-article-section__content"})
    abstract = abstract_tag.get_text(strip=True) if abstract_tag else ""

    articles.append((title, abstract))

# Save to file (only title and abstract)
save_dir = "TP1/exo1/text extraction"
filename = os.path.join(save_dir, f"D_{len(articles)}.txt")
with open(filename, "w", encoding="utf-8") as f:
    for title, abstract in articles:
        f.write(f"{title}\n{abstract}\n\n")

print(f"Saved {len(articles)} articles to {filename}")
