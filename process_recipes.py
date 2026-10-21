import json
import os

input_file = 'rec.json'
output_file = 'recs.json'

def process_file():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    data = []

    # 1. Try parsing as a standard JSON file first
    try:
        data = json.loads(content)
        print("Successfully loaded as standard JSON.")
    except json.JSONDecodeError:
        print("Standard JSON load failed. Parsing as line-by-line JSON (JSON Lines)...")
        try:
            for line in content.splitlines():
                line = line.strip()
                if line:
                    # Remove trailing comma if present in export formats
                    if line.endswith(','):
                        line = line[:-1].strip()
                    data.append(json.loads(line))
            print(f"Successfully loaded {len(data):,} rows line-by-line.")
        except Exception as e:
            print(f"Error: Could not parse file format. Details: {e}")
            return

    # Ensure data is treated as a list of records
    if not isinstance(data, list):
        data = [data]

    print(f"Processing {len(data):,} records to remove URLs...")
    url_count = 0
    cleaned_data = []

    for item in data:
        if isinstance(item, dict):
            # Find and remove any key containing 'url' (case-insensitive)
            keys_to_remove = [k for k in item.keys() if 'url' in k.lower()]
            for k in keys_to_remove:
                del item[k]
                url_count += 1
        cleaned_data.append(item)

    print(f"Removed URLs from {url_count:,} records. Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"Success! All data cleaned and saved to '{output_file}'.")

if __name__ == "__main__":
    process_file()
