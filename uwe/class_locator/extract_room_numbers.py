import fitz  # PyMuPDF
import re
import json

# Load your block template (with descriptions)
with open("rooms_by_block.json", "r") as f:
    blocks = json.load(f)

# Map block letter to block dict for quick access
block_map = {b["block"]: b for b in blocks}

# Regex to match room numbers like 1A001, 1K004A, etc.
room_number_pattern = re.compile(r'\b[0-9][A-Z]{1,2}[A-Z]?\d+[A-Z]?\b')

# List your PDF paths here
pdf_paths = [
    "FR-AtoM-01.pdf",   # Update with your actual file names/paths
    "FR-PQ-02.pdf"
]

for pdf_path in pdf_paths:
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        for match in room_number_pattern.findall(text):
            room_code = match
            # Extract block letter (first letter after digit)
            block_letter_match = re.match(r'\d+([A-Z])', room_code)
            if block_letter_match:
                block_letter = block_letter_match.group(1)
                if block_letter in block_map:
                    # Avoid duplicates
                    if "rooms" not in block_map[block_letter]:
                        block_map[block_letter]["rooms"] = []
                    if room_code not in block_map[block_letter]["rooms"]:
                        block_map[block_letter]["rooms"].append(room_code)

# Optionally, sort room numbers for each block
for block in blocks:
    block["rooms"] = sorted(block.get("rooms", []))

# Output as JSON
with open("rooms_by_block_numbers.json", "w") as f:
    json.dump(blocks, f, indent=2)

print("Extraction complete. Output written to rooms_by_block_numbers.json")