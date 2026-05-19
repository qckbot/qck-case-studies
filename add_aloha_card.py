import re

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies'
html = open(f'{base}/index.html').read()

# Find the airestech card (first card) and insert aloha before it, or find grid end
# Use airestech as anchor - insert aloha card before it
# Find the div containing airestech card
airestech_idx = html.find('href="/case-studies/airestech"')
if airestech_idx < 0:
    print("Airestech not found - trying alternate anchor")
    # Find the grid container and insert at start
else:
    # Go back to find the enclosing data-industry div
    card_start = html.rfind('<div data-industry=', 0, airestech_idx)
    if card_start < 0:
        card_start = html.rfind('<div ', 0, airestech_idx - 50)
    
    aloha_card = """<div data-industry="health ecom" data-name="aloha plant protein nutrition wellness aloha.com">
          <a href="/case-studies/aloha" class="case-card block rounded-2xl overflow-hidden card-hover h-full" style="background:#111827; border:1px solid #1f2937;">
            <div class="h-1" style="background:linear-gradient(90deg,#3b82f6,#22c55e)"></div>
            <div class="p-4 flex flex-col h-full">
              <div class="flex items-center justify-between mb-3 gap-2">
                <div class="flex items-center gap-2 min-w-0 flex-1">
                  <div class="w-8 h-8 rounded flex-shrink-0 flex items-center justify-center text-white font-bold text-sm" style="background:linear-gradient(135deg,#22c55e,#16a34a)">A</div>
                  <div class="min-w-0"><div class="font-bold text-white text-sm truncate">Aloha</div><div class="text-gray-600 text-xs truncate">aloha.com</div></div>
                </div>
                <span class="text-xs px-2 py-0.5 rounded-full flex-shrink-0 whitespace-nowrap" style="background:rgba(34,197,94,0.15);color:#4ade80;border:1px solid rgba(34,197,94,0.3)">Health</span>
              </div>
              <div class="grid grid-cols-2 gap-2 mb-3 flex-1">
                <div class="rounded-lg p-2.5" style="background:#0a0f1e;"><div class="text-base font-black text-green-400">+112%</div><div class="text-xs text-gray-500 leading-tight mt-0.5">in 6 months</div></div>
                <div class="rounded-lg p-2.5 flex flex-col justify-center" style="background:#0a0f1e;"><div class="text-xs text-gray-500">peak</div><div class="text-sm font-black text-blue-400">85k/mo</div></div>
              </div>
              <div class="flex items-center gap-1 text-xs font-semibold" style="color:#3b82f6;">View Case Study <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg></div>
            </div>
          </a>
        </div>
        """
    
    html_new = html[:card_start] + aloha_card + html[card_start:]
    open(f'{base}/index.html', 'w').write(html_new)
    print(f"Added Aloha card before airestech (pos {card_start})")
    
    # Verify
    assert 'case-studies/aloha' in html_new, "Aloha card not in file!"
    print("Verified: Aloha card present")
