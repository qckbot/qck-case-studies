import re, json

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'
with open('/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/batch4_competitors.json') as f:
    raw = json.load(f)
new_section = raw['koia']['competitorSection'] if isinstance(raw['koia'], dict) else raw['koia']

html = open(f'{base}/koia/index.html').read()

# Koia has a fully custom competitor section already (Orgain, Vega, Ripple) - check
comp_idx = html.lower().find('competitive landscape')
if comp_idx >= 0:
    ctx = html[comp_idx:comp_idx+1000]
    clean = re.sub(r'<[^>]+>', ' ', ctx)
    clean = re.sub(r'\s+', ' ', clean).strip()
    print("Koia already has:", clean[:300])
    print("\nSkipping koia - has real competitor section already")
else:
    # Find the challenge section paragraph
    # Look for "The challenge: owning search" or similar
    challenge = re.search(r'<p[^>]*>[^<]*(?:owning search|giants dominate|category where)[^<]*</p>', html, re.DOTALL | re.IGNORECASE)
    if challenge:
        print("Found challenge:", html[challenge.start():challenge.end()][:200])
    
    # Just find any paragraph about competing/challenge after "The Challenge" heading
    section_start = html.lower().find('the challenge')
    if section_start >= 0:
        # Find all paragraphs after the heading
        chunk = html[section_start:section_start+2000]
        paras = list(re.finditer(r'<p[^>]*>(.*?)</p>', chunk, re.DOTALL))
        if paras:
            # Replace the last paragraph in the challenge section with our competitor section
            last_para = paras[-1]
            abs_start = section_start + last_para.start()
            abs_end = section_start + last_para.end()
            html_new = html[:abs_start] + new_section + html[abs_end:]
            open(f'{base}/koia/index.html', 'w').write(html_new)
            print("Fixed koia via last-para replacement")
