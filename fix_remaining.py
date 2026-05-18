import re, json

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

with open('/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/batch4_competitors.json') as f:
    raw = json.load(f)

replacements = {}
for slug, val in raw.items():
    if isinstance(val, dict):
        replacements[slug] = val.get('competitorSection', val.get('html', ''))
    else:
        replacements[slug] = val

# These 4 have a different boilerplate - pattern 3: "The Challenge\n[brand] operates in [industry]..."
PATTERN3 = re.compile(
    r'The Challenge\s*\n?\s*<[^>]+>.*?</[^>]+>\s*.*?operates in.*?(?:Search visibility isn\'t optional.*?)\.</p>',
    re.DOTALL | re.IGNORECASE
)
# Even simpler - just find the paragraph that starts with "The challenge: ranking"
PATTERN4 = re.compile(
    r'<p[^>]*>\s*The challenge:\s*ranking.*?</p>',
    re.DOTALL | re.IGNORECASE
)
# Broadest - find "where buying intent lives"
PATTERN5 = re.compile(
    r'Search visibility isn\'t optional.*?where buying intent lives\.\s*(?:The challenge:[^<]*)?</p>',
    re.DOTALL | re.IGNORECASE
)

for slug in ['koia', 'medical-saunas', 'poplin', 'provacan']:
    new_section = replacements.get(slug, '')
    if not new_section:
        print(f"No content for {slug}")
        continue
    
    path = f'{base}/{slug}/index.html'
    html = open(path).read()
    original = html
    
    # Try to find the "The challenge: ranking..." paragraph specifically
    challenge_para = re.search(
        r'<p[^>]*>\s*(?:The challenge[^<]*(?:ranking|competing|outranking)[^<]*)</p>',
        html, re.DOTALL | re.IGNORECASE
    )
    if challenge_para:
        html = html[:challenge_para.start()] + new_section + html[challenge_para.end():]
        open(path, 'w').write(html)
        print(f"Fixed (pattern challenge-para): {slug}")
        continue
    
    # Try finding the section between "where buying intent lives" and "The Challenge" heading
    # Replace just the boilerplate challenge paragraph
    boilerplate = re.search(
        r'(Search visibility isn\'t optional[^<]*where buying intent lives\.)\s*(<p[^>]*>\s*The challenge:[^<]*</p>)',
        html, re.DOTALL | re.IGNORECASE
    )
    if boilerplate:
        # Replace the "The challenge:" paragraph with new section
        html = html[:boilerplate.start(2)] + new_section + html[boilerplate.end(2):]
        open(path, 'w').write(html)
        print(f"Fixed (pattern boilerplate2): {slug}")
        continue
    
    print(f"Still not found: {slug} — checking for manual pattern")
    # Show what we're looking at
    idx = html.lower().find('challenge')
    ctx = html[max(0,idx-20):idx+800]
    # Find all <p> tags in this section
    paras = re.findall(r'<p[^>]*>(.*?)</p>', ctx, re.DOTALL)
    for p in paras[:5]:
        clean = re.sub(r'<[^>]+>', '', p).strip()[:150]
        if clean:
            print(f"  p: {clean}")
