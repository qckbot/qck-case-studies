import re, os

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'
slugs = sorted([s for s in os.listdir(base) if s != 'index.html' and not s.startswith('.')])

issues = []

for slug in slugs:
    path = f'{base}/{slug}/index.html'
    if not os.path.exists(path):
        print(f"{slug:35} | NO index.html")
        continue
    
    html = open(path).read()
    
    title = re.search(r'<title>(.*?)</title>', html)
    title_str = title.group(1) if title else 'NO TITLE'
    
    domain_matches = re.findall(r'https?://(?:www\.)?([a-zA-Z0-9\-]+\.[a-zA-Z]{2,})', html)
    domains = [d for d in domain_matches if not any(x in d.lower() for x in ['qck','vercel','google','fonts','cdn','chart','tailwind','jquery'])]
    primary_domain = domains[0] if domains else 'UNKNOWN'
    
    months = re.findall(r'in\s+(\d+)\s+months?', html, re.IGNORECASE)
    years = re.findall(r'in\s+(\d+)\s+years?', html, re.IGNORECASE)
    
    flags = []
    if months:
        m = int(months[0])
        if m > 6:
            flags.append(f"TIMEFRAME:{m}mo")
    if years:
        flags.append(f"TIMEFRAME:{years[0]}yr")
    
    has_any_img = bool(re.search(r'<img[^>]*src=(?:"|\')', html))
    has_b64 = 'data:image' in html
    if not has_b64 and not has_any_img:
        flags.append("NO_LOGO")
    elif has_any_img and not has_b64:
        flags.append("EXT_IMG_ONLY")
    
    generic_comps = ['webmd','healthline','supplement review sites','generic wellness','amazon','wayfair']
    for gc in generic_comps:
        if gc.lower() in html.lower():
            flags.append(f"GENERIC_COMP:{gc}")
    
    flag_str = ' | '.join(flags) if flags else 'OK'
    print(f"{slug:35} | {primary_domain:30} | {flag_str}")
