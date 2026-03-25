import re
import csv

# Read the new 29-word CSV
csv_path = "/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/vocab_shuffled_30_anime.csv"
cards = []
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader) # skip header
    for row in reader:
        word = row[0]
        back_lines = [l.strip() for l in row[1].split('\n') if l.strip()]
        
        # extract english example
        english_example = ""
        for line in back_lines:
            if "【例句】" in line:
                english_example = line.replace("【例句】", "").strip()
                # Remove chinese translation part if any using simple regex or split, but it's already split by \n
                break
                
        # format as JS object string
        back_lines_js = "[" + ", ".join([f"'{l.replace(chr(39), chr(92)+chr(39))}'" for l in back_lines]) + "]"
        cards.append(f"      {{ front: '{word}', backLines: {back_lines_js}, englishExample: '{english_example.replace(chr(39), chr(92)+chr(39))}' }}")

cards_js_array = "[\n" + ",\n".join(cards) + "\n    ];"

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the BUILT_IN_CARDS array
pattern = re.compile(r"const BUILT_IN_CARDS = \[[\s\S]*?\];", re.MULTILINE)
content = pattern.sub(f"const BUILT_IN_CARDS = {cards_js_array}", content)

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Built-in cards updated.")
