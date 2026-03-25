import re

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the pollinations AI url with our local/CDN anime images
old_img = """<div class="w-full h-60 bg-slate-100 rounded-2xl mb-5 overflow-hidden shadow-md border border-slate-100 relative">
                  <div class="absolute inset-0 flex items-center justify-center text-slate-300 text-sm">載入動漫圖解中...</div>
                  <img src="https://image.pollinations.ai/prompt/high%20quality%20anime%20style%20illustration%20representing%20the%20word%20${encodeURIComponent(keyword)}?width=800&height=600&nologo=true" class="w-full h-full object-cover relative z-10" loading="lazy" alt="${keyword}" />
                </div>"""

new_img = """<div class="w-full h-60 bg-slate-100 rounded-2xl mb-5 overflow-hidden shadow-md border border-slate-100 relative">
                  <div class="absolute inset-0 flex items-center justify-center text-slate-300 text-sm">載入動漫圖解中...</div>
                  <img src="./anime-images/${encodeURIComponent(keyword.toLowerCase())}.jpg" class="w-full h-full object-cover relative z-10" loading="lazy" alt="${keyword}" onerror="this.src='https://images.unsplash.com/photo-1541562232579-512a21360020?q=80&w=400&auto=format&fit=crop'" />
                </div>"""

content = content.replace(old_img, new_img)

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "w", encoding="utf-8") as f:
    f.write(content)

print("App HTML updated to use local anime images.")
