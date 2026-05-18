"""
Extract and display the competitive landscape section from every case study.
Shows what's actually rendered to the user.
"""
import re, os, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

for path in sorted(glob.glob(f'{base}/*/index.html')):
    slug = path.split('/')[-2]
    if 'on-hold' in slug or slug == 'emer-male-clinic':
        continue
    html = open(path).read()

    # Find competitive landscape section - look for the heading
    match = re.search(
        r'(Competitive Landscape|Who They Were Up Against|The Competition|Competing Against)(.*?)(?=<h[23]|<div class="[^"]*section|audit-grid|id=")',
        html, re.IGNORECASE | re.DOTALL
    )
    if match:
        raw = match.group(0)[:2000]
        clean = re.sub(r'<[^>]+>', ' ', raw)
        clean = re.sub(r'\s+', ' ', clean).strip()[:500]
        print(f"\n{'='*60}")
        print(f"SLUG: {slug}")
        print(clean)
    else:
        # Try to find any section with competitor-like text
        idx = html.lower().find('competitor')
        if idx < 0:
            idx = html.lower().find('competing')
        if idx >= 0:
            chunk = html[max(0,idx-50):idx+800]
            clean = re.sub(r'<[^>]+>', ' ', chunk)
            clean = re.sub(r'\s+', ' ', clean).strip()[:400]
            print(f"\n{'='*60}")
            print(f"SLUG: {slug} (no heading found)")
            print(clean)
        else:
            print(f"\n{slug}: NO COMPETITOR SECTION FOUND")
