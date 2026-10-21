import json
import ast
import os

input_file = 'rec.json'

def process_recipes():
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    data = None
    # Try standard JSON parsing first, fallback to literal eval if single quotes are used
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

    cleaned_data = []
    print(f"Processing {len(data):,} records...")
    
    for item in data:
        # Skip if the item is not a dictionary (e.g. empty rows or invalid entries)
        if not isinstance(item, dict):
            continue

        # Extract target fields (ignoring 'url' and other metadata completely)
        name = item.get("name") or item.get("title")
        ingredients = item.get("ingredients")
        instructions = item.get("instructions")

        # Check if the row is effectively empty (name, ingredients, and instructions are all blank/empty)
        is_empty = True
        if name or ingredients or instructions:
            # Verify they contain actual text/data, not just empty strings or empty lists
            has_name = isinstance(name, str) and name.strip() != ""
            has_ingredients = bool(ingredients) # works for non-empty lists or strings
            has_instructions = bool(instructions)
            
            if has_name or has_ingredients or has_instructions:
                is_empty = False

        # If the row is empty, skip it (do not add to cleaned_data)
        if is_empty:
            continue

        # Build the clean item containing ONLY name, ingredients, and instructions
        cleaned_item = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions
        }
        cleaned_data.append(cleaned_item)

    print(f"Saving cleaned data back to {input_file} ({len(cleaned_data):,} valid records kept)...")
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
    
    print("Processing completed successfully!")

if __name__ == "__main__":
    process_recipes()
