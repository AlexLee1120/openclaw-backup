import re

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update handleSrsAction
old_handle = """    const handleSrsAction = async (action) => {
      state.stats[action]++;
      const currentCard = state.reviewQueue.shift();
      const qualityMap = { again: 1, hard: 2, good: 3, easy: 4 };
      updateSRS(currentCard, qualityMap[action]);

      if (action === 'again') state.reviewQueue.splice(Math.min(2, state.reviewQueue.length), 0, currentCard);
      else if (action === 'hard') state.reviewQueue.splice(Math.floor(state.reviewQueue.length / 2), 0, currentCard);
      else if (action === 'good') { if (currentCard.srs.interval < 7) state.reviewQueue.push(currentCard); }
      // Easy is mastery, removed from queue

      state.isFlipped = false;
      await saveState();
      render();
      autoSpeak();
    };"""

new_handle = """    const handleSrsAction = async (action) => {
      const cardEl = document.getElementById('flashcard');
      const actionBtns = document.getElementById('action-buttons');
      
      if (cardEl) {
        cardEl.style.transition = 'transform 0.4s ease-out, opacity 0.4s ease-out';
        cardEl.style.opacity = '0';
        if (action === 'again') cardEl.style.transform = 'rotateY(180deg) translate(-1000px, 100px) rotateZ(-30deg)';
        else if (action === 'hard') cardEl.style.transform = 'rotateY(180deg) translate(-500px, -800px) rotateZ(-15deg)';
        else if (action === 'good') cardEl.style.transform = 'rotateY(180deg) translate(500px, -800px) rotateZ(15deg)';
        else if (action === 'easy') cardEl.style.transform = 'rotateY(180deg) translate(1000px, 100px) rotateZ(30deg)';
        
        if (actionBtns) actionBtns.style.pointerEvents = 'none';
      }

      setTimeout(async () => {
        state.stats[action]++;
        const currentCard = state.reviewQueue.shift();
        const qualityMap = { again: 1, hard: 2, good: 3, easy: 4 };
        updateSRS(currentCard, qualityMap[action]);

        if (action === 'again') state.reviewQueue.splice(Math.min(2, state.reviewQueue.length), 0, currentCard);
        else if (action === 'hard') state.reviewQueue.splice(Math.floor(state.reviewQueue.length / 2), 0, currentCard);
        else if (action === 'good') { if (currentCard.srs.interval < 7) state.reviewQueue.push(currentCard); }

        state.isFlipped = false;
        await saveState();
        render();
        autoSpeak();
      }, 400);
    };"""

content = content.replace(old_handle, new_handle)

# 2. Update flashcard HTML structure
old_card_html = """            <div id="flashcard" class="relative w-full min-h-[400px] transition-all duration-500 transform-style-3d cursor-pointer ${state.isFlipped ? 'rotate-y-180' : ''}">"""

new_card_html = """            <div id="flashcard" class="relative w-full min-h-[400px] transition-all duration-500 transform-style-3d cursor-grab active:cursor-grabbing ${state.isFlipped ? 'rotate-y-180' : ''}" style="will-change: transform;">
              <!-- 提示標籤 -->
              <div id="hint-nope" class="absolute top-10 left-5 z-50 text-3xl font-black uppercase px-4 py-2 rounded-xl text-rose-500 border-4 border-rose-500 -rotate-12 opacity-0 transition-opacity pointer-events-none shadow-lg bg-white/90">忘記</div>
              <div id="hint-yep" class="absolute top-10 right-5 z-50 text-3xl font-black uppercase px-4 py-2 rounded-xl text-emerald-500 border-4 border-emerald-500 rotate-12 opacity-0 transition-opacity pointer-events-none shadow-lg bg-white/90">簡單</div>
"""

content = content.replace(old_card_html, new_card_html)

# 3. Update the back-face bottom text to indicate swipe
old_back_text = """<div class="mt-auto pt-8 grid grid-cols-4 gap-3">"""
new_back_text = """<p class="text-center text-slate-400 text-xs font-bold mb-4">[ 可左右滑動，或點擊下方按鈕 ]</p>
                <div id="action-buttons" class="mt-auto pt-4 grid grid-cols-4 gap-3">"""

content = content.replace(old_back_text, new_back_text)

# 4. Inject swipe JS logic into render
old_event_listeners = """      // Event Listeners for Dynamic UI
      const card = document.getElementById('flashcard');
      if (card) card.onclick = () => { if (!state.isFlipped) { state.isFlipped = true; render(); autoSpeak(); } };
      
      document.querySelectorAll('[data-srs]').forEach(btn => {
        btn.onclick = (e) => { e.stopPropagation(); handleSrsAction(btn.dataset.srs); };
      });"""

new_event_listeners = """      // Event Listeners for Dynamic UI
      const cardEl = document.getElementById('flashcard');
      const hintNope = document.getElementById('hint-nope');
      const hintYep = document.getElementById('hint-yep');
      
      let isDragging = false;
      let startX = 0;
      let currentX = 0;

      if (cardEl) {
        cardEl.onclick = (e) => { 
          if (Math.abs(currentX) > 10) return; 
          if (!state.isFlipped) { state.isFlipped = true; render(); autoSpeak(); } 
        };

        const dragStart = (clientX) => {
          if (!state.isFlipped) return;
          isDragging = true;
          startX = clientX;
          cardEl.style.transition = 'none';
        };

        const dragMove = (clientX) => {
          if (!isDragging || !state.isFlipped) return;
          currentX = clientX - startX;
          const rotateZ = currentX * 0.05;
          cardEl.style.transform = `rotateY(180deg) translate(${currentX}px, 0) rotateZ(${rotateZ}deg)`;

          if (currentX > 0) {
            if(hintYep) hintYep.style.opacity = Math.min(currentX / 100, 1);
            if(hintNope) hintNope.style.opacity = 0;
          } else {
            if(hintNope) hintNope.style.opacity = Math.min(Math.abs(currentX) / 100, 1);
            if(hintYep) hintYep.style.opacity = 0;
          }
        };

        const dragEnd = () => {
          if (!isDragging || !state.isFlipped) return;
          isDragging = false;
          cardEl.style.transition = 'transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
          
          const threshold = 100;
          if (currentX > threshold) {
            handleSrsAction('easy');
          } else if (currentX < -threshold) {
            handleSrsAction('again');
          } else {
            cardEl.style.transform = 'rotateY(180deg)';
            if(hintYep) hintYep.style.opacity = 0;
            if(hintNope) hintNope.style.opacity = 0;
          }
          currentX = 0;
        };

        // Touch events
        cardEl.addEventListener('touchstart', e => dragStart(e.touches[0].clientX));
        cardEl.addEventListener('touchmove', e => dragMove(e.touches[0].clientX));
        cardEl.addEventListener('touchend', dragEnd);

        // Mouse events
        const onMouseMove = e => dragMove(e.clientX);
        const onMouseUp = () => { dragEnd(); document.removeEventListener('mousemove', onMouseMove); document.removeEventListener('mouseup', onMouseUp); };
        
        cardEl.addEventListener('mousedown', e => {
          dragStart(e.clientX);
          document.addEventListener('mousemove', onMouseMove);
          document.addEventListener('mouseup', onMouseUp);
        });
      }
      
      document.querySelectorAll('[data-srs]').forEach(btn => {
        btn.onclick = (e) => { e.stopPropagation(); handleSrsAction(btn.dataset.srs); };
      });"""

content = content.replace(old_event_listeners, new_event_listeners)

# 5. Fix keydown events for grading
old_keydown = """      if (state.isFlipped && ['1','2','3','4'].includes(e.key)) {
          const map = {'1':'again', '2':'hard', '3':'good', '4':'easy'};
          handleSrsAction(map[e.key]);
      }"""

new_keydown = """      if (state.isFlipped) {
          const map = {'1':'again', '2':'hard', '3':'good', '4':'easy', 'ArrowLeft':'again', 'ArrowRight':'easy'};
          if (map[e.key]) handleSrsAction(map[e.key]);
      }"""

content = content.replace(old_keydown, new_keydown)

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/app.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Update complete")
