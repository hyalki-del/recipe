from bs4 import BeautifulSoup
import json
import requests
import time

BASE_URL = "https://www.ardaninmutfagi.com/category/yemek-tarifleri/page/{}/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
}


def scrape_recipes():
  recipes = []

  # For a test, loop through the first 2 pages. Increase this range to get more.
  for page in range(1, 3):
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
      break

    soup = BeautifulSoup(response.text, "html.parser")

    # Find recipe blocks (adjust selectors based on exact site layout)
    posts = soup.find_all("div", class_="post-summary") or soup.find_all(
        "article"
    )

    for post in soup.select("h2.entry-title a"):
      title = post.text.strip()
      link = post.get("href")

      # Scrape individual recipe page details
      recipe_data = get_recipe_details(link, title)
      if recipe_data:
        recipes.append(recipe_data)

      time.sleep(1)  # Be polite to the server

  # Save to recipes.json
  with open("recipes.json", "w", encoding="utf-8") as f:
    json.dump(recipes, f, ensure_ascii=False, indent=4)

  print(f"Successfully saved {len(recipes)} recipes to recipes.json")


def get_recipe_details(url, title):
  try:
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    # Extract ingredients (typically inside the content area)
    content = soup.find("div", class_="entry-content")
    ingredients = []
    if content:
      # Simple heuristic: grab paragraphs or list items
      for p in content.find_all(["p", "li"]):
        text = p.text.strip()
        if "malzemeler" in text.lower() or len(ingredients) > 0:
          ingredients.append(text)

    return {"title": title, "url": url, "ingredients": ingredients[:15]}
  except Exception as e:
    print(f"Error scraping {url}: {e}")
    return None


if __name__ == "__main__":
  scraper_recipes() if "scraper_recipes" in globals() else scrape_recipes()
