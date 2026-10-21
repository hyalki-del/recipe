import json
import ast
import os

input_file = 'rec.json'
output_file = 'recs.json'

def clean_recipes():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    data = None
    
    # Attempt 1: Standard JSON load
    try:
        data = json.loads(content)
        print("Successfully loaded using standard JSON parser.")
    except json.JSONDecodeError as e:
        print(f"Standard JSON load failed: {e}")
        print("Attempting to parse as Python literal structure...")
        try:
            data = ast.literal_eval(content)
            print("Successfully loaded using Python literal evaluator.")
        except Exception as err:
            print(f"Error: Could not parse file. Details: {err}")
            return

    if not isinstance(data, list):
        print("Error: The loaded data is not a list of recipes.")
        return

    print(f"Processing {len(data):,} records to remove URLs...")
    
    url_count = 0
    cleaned_data = []
    
    for item in data:
        if isinstance(item, dict):
            # Remove any key that is 'url' or contains 'url' (case-insensitive)
            keys_to_remove = [k for k in item.keys() if 'url' in k.lower()]
            for k in keys_to_remove:
                del item[k]
                url_count += 1
        cleaned_data.append(item)

    print(f"Removed URLs from {url_count:,} records. Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    
    print(f"Success! All remaining info has been written to '{output_file}'.")

if __name__ == "__main__":
    clean_recipes()
