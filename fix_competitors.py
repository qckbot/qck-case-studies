"""
Audit script: identify exactly which case studies have generic/placeholder competitor sections
so CC can fix them with real content.
"""
import re, os, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

GENERIC_TERMS = [
    'webmd', 'healthline', 'supplement review sites', 'generic wellness brands',
    'generic wellness', 'amazon.com', 'wayfair', 'generic brand',
    'major retailers', 'big box stores', 'placeholder', 'lorem ipsum',
    'your competitor', 'competitor 1', 'competitor 2',
    'supplement brands', 'wellness brands', 'health brands',
]

results = []
for path in sorted(glob.glob(f'{base}/*/index.html')):
    slug = path.split('/')[-2]
    html = open(path).read()
    
    found = []
    for term in GENERIC_TERMS:
        if term.lower() in html.lower():
            # Get context around the term
            idx = html.lower().find(term.lower())
            context = html[max(0,idx-50):idx+100].replace('\n',' ').strip()
            found.append(f"  '{term}' -> ...{context}...")
    
    if found:
        results.append((slug, found))
        print(f"\n{slug}:")
        for f in found[:3]:  # Show first 3
            print(f)

print(f"\n\nTotal case studies with generic content: {len(results)}")
for slug, _ in results:
    print(f"  - {slug}")
