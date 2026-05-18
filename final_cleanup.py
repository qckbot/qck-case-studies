import re, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

# DIP, FOCL, Vivazen still have boilerplate but also have new competitor sections
# Just strip the boilerplate text
for slug in ['dip', 'focl', 'vivazen']:
    path = f'{base}/{slug}/index.html'
    html = open(path).read()
    original = html
    # Remove all forms of boilerplate
    html = re.sub(
        r'<p[^>]*>[^<]*Being absent from page 1[^<]*</p>',
        '', html, flags=re.DOTALL | re.IGNORECASE
    )
    html = re.sub(
        r"<p[^>]*>[^<]*Search visibility isn't optional[^<]*</p>",
        '', html, flags=re.DOTALL | re.IGNORECASE
    )
    html = re.sub(
        r'<p[^>]*>[^<]*The challenge:\s*ranking for competitive[^<]*</p>',
        '', html, flags=re.DOTALL | re.IGNORECASE
    )
    if html != original:
        open(path, 'w').write(html)
        print(f"Cleaned: {slug}")
    else:
        print(f"No change: {slug}")
