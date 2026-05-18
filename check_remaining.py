import re, os, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'
BOILERPLATE_TEXT = 'Being absent from page 1 means losing customers'
ALT_BOILERPLATE = 'Search visibility isn\'t optional; it\'s where buying intent lives'

still_generic = []
for path in sorted(glob.glob(f'{base}/*/index.html')):
    slug = path.split('/')[-2]
    if 'on-hold' in slug or slug == 'emer-male-clinic':
        continue
    html = open(path).read()
    if BOILERPLATE_TEXT in html or ALT_BOILERPLATE in html:
        # Check if it has a real competitor section too
        has_comp = bool(re.search(r'Competitive Landscape', html, re.IGNORECASE))
        still_generic.append((slug, has_comp))

print(f"Still have boilerplate: {len(still_generic)}")
for slug, has_comp in still_generic:
    print(f"  {slug} (has comp section: {has_comp})")
