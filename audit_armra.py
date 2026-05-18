"""Check ARMRA specifically for the bad content Robert flagged"""
import re

html = open('/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies/armra/index.html').read()

# Find all text content near webmd/healthline
for term in ['webmd', 'healthline', 'supplement review', 'generic wellness']:
    idx = html.lower().find(term.lower())
    if idx >= 0:
        context = html[max(0,idx-200):idx+300]
        clean = re.sub(r'<[^>]+>', ' ', context)
        clean = re.sub(r'\s+', ' ', clean).strip()
        print(f"=== '{term}' found ===")
        print(clean[:400])
        print()

# Also print competitive section
comp_idx = html.lower().find('competitor')
if comp_idx >= 0:
    chunk = html[max(0,comp_idx-100):comp_idx+2000]
    clean = re.sub(r'<[^>]+>', ' ', chunk)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print("=== COMPETITOR SECTION ===")
    print(clean[:600])
