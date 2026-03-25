import csv
import random

file_path = "/Users/alex-ai/.openclaw/workspace/assets/srs-data/SRS_Pro_核心單字_1000字完整版.csv"
out_path = "/Users/alex-ai/.openclaw/workspace/assets/srs-data/SRS_Pro_核心單字_1000字完整版_亂序.csv"

with open(file_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = [row for row in reader if row] # filter empty lines

# Ensure unique words
unique_rows = []
seen_words = set()
for r in rows:
    word = r[0].strip().lower()
    if word not in seen_words:
        seen_words.add(word)
        unique_rows.append(r)

random.shuffle(unique_rows)

with open(out_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(unique_rows)

print(f"Total unique shuffled words: {len(unique_rows)}")
