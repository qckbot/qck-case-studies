"""
Deep audit: extract the actual competitive landscape section from each case study
to see what named competitors are listed.
"""
import re, os, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

BAD_GENERIC = [
    'webmd', 'healthline', 'supplement review sites', 'generic wellness brands',
    'generic wellness brand', 'wayfair', 'big box', 'major retailer',
    'lorem ipsum', 'placeholder'
]

bad_cases = []
for path in sorted(glob.glob(f'{base}/*/index.html')):
    slug = path.split('/')[-2]
    if 'on-hold' in slug or slug == 'emer-male-clinic':
        continue
    html = open(path).read()
    
    # Find competitive landscape / competitor section
    # Look for section heading
    comp_section = re.search(
        r'(?:competitive\s+landscape|competitors?|competing\s+against|competing\s+brands?)(.*?)(?:<h[23]|<section|competitor-section|$)',
        html, re.IGNORECASE | re.DOTALL
    )
    
    if comp_section:
        section_text = re.sub(r'<[^>]+>', ' ', comp_section.group(0))
        section_text = re.sub(r'\s+', ' ', section_text).strip()[:300]
        
        has_bad = any(b.lower() in section_text.lower() for b in BAD_GENERIC)
        if has_bad:
            bad_cases.append(slug)
            print(f"\n{slug}:")
            print(f"  {section_text[:200]}")

print(f"\n\nBad competitor sections: {len(bad_cases)}")
for s in bad_cases:
    print(f"  {s}")
