import re
html = open('/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies/airestech/index.html').read()
# Find what the challenge/competitor section actually says
idx = html.lower().find('competitor')
if idx >= 0:
    ctx = html[max(0,idx-200):idx+500]
    clean = re.sub(r'<[^>]+>', ' ', ctx)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print("Competitor context:", clean[:400])

# Also look for any 'challenge' section
idx2 = html.lower().find('challenge')
if idx2 >= 0:
    ctx2 = html[max(0,idx2-100):idx2+600]
    clean2 = re.sub(r'<[^>]+>', ' ', ctx2)
    clean2 = re.sub(r'\s+', ' ', clean2).strip()
    print("\nChallenge context:", clean2[:400])

# Find unique paragraphs 
paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
for p in paras[:20]:
    clean = re.sub(r'<[^>]+>', '', p).strip()[:150]
    if clean:
        print(f"  P: {clean[:100]}")
