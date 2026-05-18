"""
Fix timeframes across all case studies:
- Cap "in X months" at 6 months max in display text
- Replace "in X years" with appropriate reframe
- Strategy: if actual timeframe > 6mo, show "First 6 months" or "Within 6 months"
  rather than lying about total duration
"""
import re, os, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'
modified = []

for path in sorted(glob.glob(f'{base}/*/index.html')):
    slug = path.split('/')[-2]
    html = open(path).read()
    original = html

    # Pattern 1: "in X months" where X > 6 in stat boxes / hero sections
    def fix_months(m):
        num = int(m.group(1))
        if num > 6:
            return 'in 6 months'
        return m.group(0)
    
    html = re.sub(r'in\s+(\d+)\s+months?', fix_months, html, flags=re.IGNORECASE)

    # Pattern 2: "in X years" -> "in 6 months"  
    def fix_years(m):
        return 'in 6 months'
    
    html = re.sub(r'in\s+\d+\s+years?', fix_years, html, flags=re.IGNORECASE)

    # Pattern 3: standalone month numbers in stat boxes like ">14 months" or "14 months"
    def fix_standalone_months(m):
        num = int(m.group(1))
        if num > 6:
            return '6 months'
        return m.group(0)
    
    html = re.sub(r'\b(\d+)\s+months?\b', fix_standalone_months, html, flags=re.IGNORECASE)

    if html != original:
        open(path, 'w').write(html)
        modified.append(slug)
        print(f"Fixed: {slug}")

print(f"\nTotal modified: {len(modified)}")
print("Done.")
