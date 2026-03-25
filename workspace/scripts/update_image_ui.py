import re

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update image container size and image source
old_img_container = """<div class="w-full h-40 bg-slate-100 rounded-2xl mb-6 overflow-hidden shadow-inner">
                  <img src="https://loremflickr.com/600/400/${encodeURIComponent(keyword)}" class="w-full h-full object-cover" />
                </div>"""

new_img_container = """<div class="w-full h-60 bg-slate-100 rounded-2xl mb-5 overflow-hidden shadow-md border border-slate-100 relative">
                  <div class="absolute inset-0 flex items-center justify-center text-slate-300 text-sm">載入動漫圖解中...</div>
                  <img src="https://image.pollinations.ai/prompt/high%20quality%20anime%20style%20illustration%20representing%20the%20word%20${encodeURIComponent(keyword)}?width=800&height=600&nologo=true" class="w-full h-full object-cover relative z-10" loading="lazy" alt="${keyword}" />
                </div>"""

content = content.replace(old_img_container, new_img_container)

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Image UI updated")
