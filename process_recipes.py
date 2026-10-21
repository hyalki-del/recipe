import json
import os

input_file = 'rec.json'

def process_recipes():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = []
    print(f"Processing {len(data):,} records...")
    
    for item in data:
        # Extracts only the essential fields and drops URLs/metadata
        cleaned_item = {
            "name": item.get("name") or item.get("title"),
            "ingredients": item.get("ingredients"),
            "instructions": item.get("instructions")
        }
        cleaned_data.append(cleaned_item)

    print(f"Saving cleaned data back to {input_file}...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    
    print("Processing complete successfully!")

if __name__ == "__main__":
    process_recipes()
