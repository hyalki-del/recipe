import json
import ast
import os

input_file = 'rec.json'
output_file = 'recs.json'

def process_file():
    if not os.path.exists(input_file):
        print(f"CRITICAL ERROR: '{input_file}' does not exist in the repository.")
        return

    print(f"Loading '{input_file}'...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    data = None

    # Step 1: Try standard JSON parsing
    try:
        data = json.loads(content)
        print("-> Successfully loaded as standard JSON.")
    except Exception as e1:
        print(f"-> Standard JSON load failed: {e1}")
        
        # Step 2: Try Python literal eval (handles single quotes and Python dict exports)
        try:
            print("-> Attempting to parse as Python literal structure (single quotes)...")
            data = ast.literal_eval(content)
            print("-> Successfully loaded using ast.literal_eval.")
        except Exception as e2:
            print(f"-> Python literal eval failed: {e2}")
            
            # Step 3: Try line-by-line JSON (JSON Lines format)
            try:
                print("-> Attempting to parse line-by-line (JSONL)...")
                data = []
                for line in content.splitlines():
                    line = line.strip()
                    if line:
                        if line.endswith(','):
                            line = line[:-1].strip()
                        try:
                            data.append(json.loads(line))
                        except Exception:
                            pass
                print(f"-> Successfully loaded {len(data):,} rows line-by-line.")
            except Exception as e3:
                print(f"-> Line-by-line parse failed: {e3}")

    # Validate that we successfully loaded data into a list
    if not data or not isinstance(data, list):
        print(f"CRITICAL ERROR: Could not parse '{input_file}' into a valid list of records. Data type found: {type(data)}")
        return

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

    print(f"Removed URLs from {url_count:,} records. Writing to '{output_file}'...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    # Verify output file
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"SUCCESS! '{output_file}' created successfully. File size: {file_size:,} bytes.")
    else:
        print(f"ERROR: Failed to generate '{output_file}'.")

if __name__ == "__main__":
    process_file()
