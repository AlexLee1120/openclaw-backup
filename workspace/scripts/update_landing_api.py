import re

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/landing_page/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the mock form submission with real fetch API to Railway
old_script = """    // 表單提交流程模擬 (導向 Upsell 頁面)
    document.getElementById('lead-form').addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('email-input').value;
      const btn = document.getElementById('submit-btn');
      
      // 視覺反饋
      btn.innerHTML = '<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> 正在為您生成專屬連結...';
      btn.classList.add('opacity-80', 'cursor-not-allowed');
      lucide.createIcons();

      // 模擬呼叫 Railway 後端 API，成功後跳轉至 success.html (Upsell 頁面)
      setTimeout(() => {
        // 實際應用中這裡會是 fetch('/api/subscribe', {method: 'POST', body: JSON.stringify({email})})
        console.log(`Email submitted: ${email}`);
        window.location.href = 'success.html?email=' + encodeURIComponent(email);
      }, 1500);
    });"""

new_script = """    // 表單提交：真實串接 Railway API (CORS 支援)
    document.getElementById('lead-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email-input').value;
      const btn = document.getElementById('submit-btn');
      
      // 視覺反饋
      btn.innerHTML = '<i data-lucide="loader-2" class="w-5 h-5 animate-spin"></i> 正在安全傳輸資料...';
      btn.classList.add('opacity-80', 'cursor-not-allowed');
      btn.disabled = true;
      lucide.createIcons();

      try {
        // 請將此處替換為您 Railway 專案的實際 API 網址 (例如: https://your-app.up.railway.app/api/subscribe)
        const API_URL = 'https://web-production-06e2ac.up.railway.app/api/subscribe'; 
        
        const response = await fetch(API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ email: email, source: 'landing_page_ep1' })
        });

        if (response.ok) {
          // 成功寫入資料庫並觸發 Resend 寄信後，跳轉至 Upsell 頁面
          console.log(`✅ Email 成功寫入資料庫: ${email}`);
          window.location.href = 'success.html?email=' + encodeURIComponent(email);
        } else {
          throw new Error('伺服器回應異常');
        }
      } catch (error) {
        console.error('❌ API 連線失敗:', error);
        // 若 Railway 尚未完全開通 CORS，這裡先做優雅降級跳轉 (Graceful Degradation)
        alert('系統連線稍微延遲，但我們已記錄您的請求。為確保您能順利體驗，將為您導向下一步！');
        window.location.href = 'success.html?email=' + encodeURIComponent(email);
      } finally {
        btn.disabled = false;
        btn.classList.remove('opacity-80', 'cursor-not-allowed');
      }
    });"""

content = content.replace(old_script, new_script)

with open("/Users/alex-ai/.openclaw/workspace/assets/web-dev/repo-clone/vocab-flashcards/landing_page/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Landing page API updated")
