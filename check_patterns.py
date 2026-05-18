import re

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'
for slug in ['koia', 'medical-saunas', 'poplin', 'provacan']:
    html = open(f'{base}/{slug}/index.html').read()
    # Find challenge/intro section
    idx = html.lower().find('challenge')
    if idx < 0:
        idx = html.lower().find('competitor')
    if idx >= 0:
        ctx = html[max(0,idx-100):idx+600]
        clean = re.sub(r'<[^>]+>', ' ', ctx)
        clean = re.sub(r'\s+', ' ', clean).strip()
        print(f"\n{slug}:")
        print(clean[:400])
    # Check for boilerplate variant
    variants = ['absent from page', 'outranking established', 'content authority and domain strength']
    for v in variants:
        if v in html.lower():
            idx2 = html.lower().find(v)
            ctx2 = html[max(0,idx2-50):idx2+300]
            clean2 = re.sub(r'<[^>]+>', ' ', ctx2)
            clean2 = re.sub(r'\s+', ' ', clean2).strip()
            print(f"  Boilerplate variant '{v}':")
            print(f"  {clean2[:200]}")
            break
