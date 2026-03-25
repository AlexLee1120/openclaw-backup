import csv
import os

input_csv = "/Users/alex-ai/.openclaw/workspace/assets/srs-data/SRS_Pro_核心單字_1000字完整版_亂序.csv"
output_csv = "/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/vocab_shuffled_30_anime.csv"
img_dir = "/Users/alex-ai/.openclaw/workspace/assets/srs-data/anime-images"

with open(input_csv, "r", encoding="utf-8") as f_in, open(output_csv, "w", encoding="utf-8", newline="") as f_out:
    reader = csv.reader(f_in)
    writer = csv.writer(f_out)
    
    header = next(reader)
    # Rewrite header for clarity in app.html parser if needed, but app.html uses column index
    writer.writerow(header)
    
    count = 0
    for row in reader:
        word = row[0].strip().lower()
        img_path = os.path.join(img_dir, f"{word}.jpg")
        
        # Only include words that successfully generated an image
        if os.path.exists(img_path):
            # Format backLines as per app.html expectation:
            # frontText = row[0]
            # backRaw = row[1] -> Split by \n, looking for 【例句】
            # Let's pack columns 1..4 into a single string for column 1
            pos = row[1]
            meaning = row[2]
            sentence = row[3]
            translation = row[4]
            
            back_combined = f"{word} ({pos}) {meaning}\n【例句】 {sentence}\n{translation}"
            writer.writerow([word, back_combined])
            
            count += 1
            if count >= 29:
                break
print(f"Created {count} records in new CSV.")
