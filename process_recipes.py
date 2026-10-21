import json
import ast
import os
import sys

input_file = 'rec.json'
output_file = 'recs.json'

def process_file():
    # 1. Check if input file exists
    if not os.path.exists(input_file):
        print(f"CRITICAL ERROR: '{input_file}' not found in the repository root directory.")
        sys.exit(1)

    print(f"Loading '{input_file}' (Size: {os.path.getsize(input_file):,} bytes)...")
    
    # 2. Read file safely with encoding fallback
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to read '{input_file}': {e}")
        sys.exit(1)

    data = None

    # 3. Try parsing methods
    try:
        data = json.loads(content)
        print("-> Successfully parsed as standard JSON.")
    except Exception as e1:
        print(f"-> Standard JSON parse failed: {e1}")
        try:
            print("-> Attempting to parse as Python literal structure...")
            data = ast.literal_eval(content)
            print("-> Successfully parsed as Python literal.")
        except Exception as e2:
            print(f"-> Python literal parse failed: {e2}")
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
                print(f"-> Successfully parsed {len(data):,} lines line-by-line.")
            except Exception as e3:
                print(f"-> Line-by-line parse failed: {e3}")

    # 4. Validate parsed data
    if not data or not isinstance(data, list):
        print(f"CRITICAL ERROR: Could not convert file content into a valid list of records. Data type: {type(data)}")
        sys.exit(1)

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

    print(f"Removed URLs from {url_count:,} records. Saving to '{output_file}'...")
    
    # 5. Write output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to write output file '{output_file}': {e}")
        sys.exit(1)

    # 6. Final verification
    if os.path.exists(output_file):
        print(f"SUCCESS! '{output_file}' created successfully. File size: {os.path.getsize(output_file):,} bytes.")
    else:
        print(f"CRITICAL ERROR: Output file '{output_file}' was not created.")
        sys.exit(1)

if __name__ == "__main__":
    process_file()
