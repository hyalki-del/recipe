from bs4 import BeautifulSoup
import json
import requests
import time

BASE_URL = "https://www.ardaninmutfagi.com/category/yemek-tarifleri/page/{}/"

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


def scrape_recipes():
  recipes = []
  print("🚀 Starting GitHub Actions scraper for Arda'nın Mutfağı...")

  # Loop through the first 3 pages (you can increase this range later)
  for page in range(1, 4):
    url = BASE_URL.format(page)
    print(f"Fetching: {url}")

    try:
      response = requests.get(url, headers=HEADERS, timeout=15)
      print(f"HTTP Status Code: {response.status_code}")

      if response.status_code != 200:
        print(f"⚠️ Warning: Non-200 status code received: {response.status_code}")
        break

      soup = BeautifulSoup(response.text, "html.parser")
      found_on_page = 0

      # Search for anchor tags across the page to extract recipe links dynamically
      for tag in soup.find_all("a", href=True):
        href = tag["href"]
        title = tag.get_text().strip()

        # Filter to isolate actual recipe pages and ignore system links
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

      print(f"-> Found {found_on_page} recipe links on page {page}")
      time.sleep(2)  # Polite pause

    except Exception as e:
      print(f"❌ Error scraping page {page}: {e}")

  # Save results to recipes.json
  with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)

  print(f"✨ Finished! Total unique recipes collected: {len(recipes)}")


if __name__ == "__main__":
  scrape_recipes()
