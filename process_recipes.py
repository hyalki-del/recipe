import json
import ast
import os

input_file = 'rec.json'

def remove_urls():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    data = None
    # Try standard JSON parsing first, fallback to Python literal if needed
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

    print(f"Processing {len(data):,} records to remove URLs...")
    
    url_count = 0
    for item in data:
        if isinstance(item, dict):
            # Find and remove any key named 'url' (case-insensitive)
            keys_to_remove = [k for k in item.keys() if k.lower() == 'url']
            for k in keys_to_remove:
                del item[k]
                url_count += 1

    print(f"Removed URLs from {url_count:,} records. Saving updated file...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Done! All URLs have been removed successfully.")

if __name__ == "__main__":
    remove_urls()
