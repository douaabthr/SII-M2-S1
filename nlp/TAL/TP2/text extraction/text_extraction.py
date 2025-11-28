from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

# Main journal volumes/issue page
myurl = "https://link.springer.com/journal/12065/volumes-and-issues"

html = urlopen(myurl).read()
soup = BeautifulSoup(html, "html.parser")

base_dir = "D:/study/nlp/TAL/TP2/text extraction"
os.makedirs(base_dir, exist_ok=True)

volumes = soup.select("li:has(h2 span)")

print("📚 Found Volumes:\n")

for volume in volumes:
    heading = volume.find("h2", {"class": "eds-c-section-heading"})
    if heading:
        span = heading.find("span")
        if span:
            print(span.get_text(strip=True))
for volume in volumes:
    i = 1
    # Get the volume title
    volume_number = volume.find("h2", {"class": "eds-c-section-heading"}).find("span").get_text(strip=True)
    print(f"\n🔹 Scraping {volume_number}")

    # Create folder for this volume
    volume_dir = os.path.join(base_dir, volume_number)
    os.makedirs(volume_dir, exist_ok=True)

    # Get issue list
    issues = volume.find_all('a', {"class": "c-list-group__link"})

    # Reverse issues for all volumes 
    issues = list(reversed(issues))

    for a in issues:
        href = a.get('href')
        if not href:
            continue

        issue_url = "https://link.springer.com" + href
        print(f"\n📘 Issue: {issue_url}")

        # Load issue page
        issue_html = urlopen(issue_url).read()
        issue_soup = BeautifulSoup(issue_html, "html.parser")

        # Find all article cards
        h3_tags = issue_soup.find_all("h3", {"class": "app-card-open__heading"})

        if not h3_tags:
            print("⚠️ No articles found in this issue.")
            continue

        # For Volume 18: reverse articles too
        if "18" in volume_number:
            h3_tags = list(reversed(h3_tags))

        for h3_tag in h3_tags:
            title = h3_tag.get_text(strip=True)
            article_link = "https://link.springer.com" + h3_tag.find('a')['href']
             # 🚫 Skip retracted or withdrawn articles
            if "RETRACTED" in title.upper() or "WITHDRAWN" in title.upper():
                print(f"   ⏩ Skipped retracted article: {title}")
                continue
            # Load article page
            article_html = urlopen(article_link).read()
            article_soup = BeautifulSoup(article_html, "html.parser")

            # Try to extract abstract
            abstract_tag = article_soup.find("div", {"class": "c-article-section__content"})
            if abstract_tag:
                abstract = abstract_tag.get_text(strip=True)
            else:
                abstract = None
                print(f"   ⚠️ No abstract for: {title}")

            # Save title & (if available) abstract to file
            filename = os.path.join(volume_dir, f"{i}.txt")
            i += 1
            with open(filename, "w", encoding="utf-8") as f:
                f.write(title)
                if abstract:
                    f.write(f"\n\n{abstract}\n")

            print(f"   💾 Saved {filename}")

        print(f"✅ Finished scraping issue: {issue_url}")

    print(f"🎉 Finished volume: {volume_number}")
