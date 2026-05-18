import re, json

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

with open('/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/batch4_competitors.json') as f:
    raw = json.load(f)

# Handle nested dict format
replacements = {}
for slug, val in raw.items():
    if isinstance(val, dict):
        replacements[slug] = val.get('competitorSection', val.get('html', str(val)))
    else:
        replacements[slug] = val

BOILERPLATE_PATTERN = re.compile(
    r'<p[^>]*>\s*Being absent from page 1 means losing customers.*?real buyer search behavior[^<]*(?:targeting[^<]*)?\s*</p>',
    re.DOTALL | re.IGNORECASE
)
BOILERPLATE_PATTERN2 = re.compile(
    r'Being absent from page 1 means losing customers.*?real buyer search behavior[^.]*\.',
    re.DOTALL | re.IGNORECASE
)

modified = []
for slug, new_section in replacements.items():
    path = f'{base}/{slug}/index.html'
    try:
        html = open(path).read()
    except FileNotFoundError:
        print(f"Not found: {slug}")
        continue
    replaced = False
    for pat in [BOILERPLATE_PATTERN, BOILERPLATE_PATTERN2]:
        match = pat.search(html)
        if match:
            html = html[:match.start()] + new_section + html[match.end():]
            replaced = True
            break
    if replaced:
        open(path, 'w').write(html)
        modified.append(slug)
        print(f"Fixed: {slug}")
    else:
        print(f"Pattern not found: {slug}")
print(f"\nModified: {len(modified)}/{len(replacements)}")
