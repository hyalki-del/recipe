from bs4 import BeautifulSoup
import json
import requests
import time

BASE_URL = (
    "https://www.ardaninmutfagi.com/category/yemek-tarifleri/page/{}/"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    ),
}


def scrape_all_recipes():
  recipes = []
  page = 1
  print(
      "🚀 Starting full scraper for Arda'nın Mutfağı (fetching all pages)..."
  )

  while True:
    url = BASE_URL.format(page)
    print(f"Fetching page {page}: {url}")

    try:
      response = requests.get(url, headers=HEADERS, timeout=15)

      # WordPress typically returns a 404 when you go past the last page
      if response.status_code != 200:
        print(
            f"🏁 Reached the end of the archive (HTTP Status Code:"
            f" {response.status_code}). Stopping."
        )
        break

      soup = BeautifulSoup(response.text, "html.parser")
      found_on_page = 0

      # Extract recipe links dynamically
      for tag in soup.find_all("a", href=True):
        href = tag["href"]
        title = tag.get_text().strip()

        if "ardaninmutfagi.com" in href:
          if (
              "/category/" not in href
              and "/tag/" not in href
              and "/page/" not in href
              and href != "https://www.ardaninmutfagi.com/"
              and len(title) > 5
          ):
            # Avoid duplicate URLs
            if not any(r["url"] == href for r in recipes):
              recipes.append({"title": title, "url": href, "ingredients": []})
              found_on_page += 1

      print(f"-> Found {found_on_page} unique new recipe links on page {page}")

      # If a page returns 0 recipes, we've hit the end
      if found_on_page == 0:
        print("No more recipes found on this page. Finishing up.")
        break

      page += 1
      time.sleep(1.5)  # Polite pause between pages to prevent getting blocked

    except Exception as e:
      print(f"❌ Error scraping page {page}: {e}")
      break

  # Save all accumulated recipes to recipes.json
  with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)

  print(f"✨ Success! Total recipes collected from all pages: {len(recipes)}")


if __name__ == "__main__":
  scrape_all_recipes()
