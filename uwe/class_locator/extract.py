import fitz  # PyMuPDF
import re
import json

# Static block descriptions (from your sample)
blocks_template = [
    {"block": "A", "description": "Located near the main entrance, beside the Students’ Union", "rooms": []},
    {"block": "B", "description": "Next to Block A, close to the main bus station", "rooms": []},
    {"block": "C", "description": "Opposite the Library, near the North Gatehouse", "rooms": []},
    {"block": "D", "description": "Close to Block C and the Information Point", "rooms": []},
    {"block": "E", "description": "Near the Library, facing the Wildlife Garden", "rooms": []},
    {"block": "F", "description": "Adjacent to Block E, beside the central courtyard", "rooms": []},
    {"block": "G", "description": "Located near the Sports and Leisure centre", "rooms": []},
    {"block": "H", "description": "Close to the East Gatehouse and Cycle Parking area", "rooms": []},
    {"block": "I", "description": "Beside Block H, near the Staff Car Park", "rooms": []},
    {"block": "J", "description": "Near the Sanctuary Spaces, opposite the Cafe", "rooms": []},
    {"block": "K", "description": "Located near Future Space and Engineering buildings", "rooms": []},
    {"block": "L", "description": "On the 1st floor near IT Services and Student Administration", "rooms": []},
    {"block": "M", "description": "Adjacent to Block L, opposite the Bus Station", "rooms": []},
    {"block": "P", "description": "On the 2nd floor of the Science block, near Future Space", "rooms": []},
    {"block": "Q", "description": "Adjacent to Block P, behind the Library", "rooms": []}
]

# Map block letter to block dict for quick access
block_map = {b["block"]: b for b in blocks_template}

# PDF extraction
pdf_path = "FR-AtoM-01.pdf"
doc = fitz.open(pdf_path)

# Pattern for the start of a room entry
room_start_pattern = re.compile(r'(\b[0-9][A-Z]{1,2}[A-Z]?\d+[A-Z]?\b)\s+\S+\s*:\s*(.+)')

for page in doc:
    lines = page.get_text().splitlines()
    i = 0
    while i < len(lines):
        match = room_start_pattern.match(lines[i])
        if match:
            room_code = match.group(1)
            room_name_lines = [match.group(2).strip()]
            # Collect subsequent lines as part of the room name until a new room or empty line
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line or room_start_pattern.match(lines[i]):
                    break
                room_name_lines.append(next_line)
                i += 1
            room_name = " ".join(room_name_lines)
            block_letter_match = re.match(r'\d+([A-Z])', room_code)
            if block_letter_match:
                block_letter = block_letter_match.group(1)
                if block_letter in block_map:
                    block_map[block_letter]["rooms"].append({
                        "room_code": room_code,
                        "name": room_name
                    })
        else:
            i += 1

# Output as JSON
with open("rooms_by_block.json", "w") as f:
    json.dump(list(block_map.values()), f, indent=2)

print("Extraction complete. Output written to rooms_by_block.json")