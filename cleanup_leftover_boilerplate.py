import re, glob

base = '/Users/clawdbot/.openclaw/workspace/builds/qck-case-studies/case-studies'

# For medical-saunas, poplin, provacan — they now have real competitor sections 
# but still have the old boilerplate elsewhere (different instance). Remove it.
BOILERPLATE_TEXT = 'Being absent from page 1 means losing customers'
ALT_BOILERPLATE = "Search visibility isn't optional; it's where buying intent lives"

# Pattern to remove the alt boilerplate paragraph
ALT_PAT = re.compile(
    r'<p[^>]*>[^<]*(?:Search visibility isn\'t optional.*?where buying intent lives\.)[^<]*</p>',
    re.DOTALL | re.IGNORECASE
)
# Also the "The challenge: ranking..." follow-up paragraph if it's the alt version
CHALLENGE_PAT = re.compile(
    r'<p[^>]*>\s*The challenge:\s*ranking for competitive[^<]*</p>',
    re.DOTALL | re.IGNORECASE
)

for slug in ['medical-saunas', 'poplin', 'provacan']:
    path = f'{base}/{slug}/index.html'
    html = open(path).read()
    original = html
    
    # Remove the alt boilerplate paragraph
    html = ALT_PAT.sub('', html)
    # Remove lingering "The challenge: ranking for competitive..." paragraph
    html = CHALLENGE_PAT.sub('', html)
    # Also remove any remaining "Being absent" text
    html = re.sub(
        r'<p[^>]*>[^<]*Being absent from page 1[^<]*</p>',
        '', html, flags=re.DOTALL | re.IGNORECASE
    )
    
    if html != original:
        open(path, 'w').write(html)
        print(f"Cleaned: {slug}")
    else:
        print(f"No change: {slug}")

# DIP and FOCL - these are minimal pages, add basic competitor section
# DIP = DIP Devices, cannabis vaporizer/concentrate accessories
# FOCL = FOCL CBD wellness brand
dip_section = "<div class='competitor-section'><h3 class='text-xl font-bold text-white mb-4'>The Competitive Landscape</h3><div class='grid grid-cols-1 md:grid-cols-3 gap-4 mb-6'><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>Puffco</div><div class='text-xs text-blue-400 mb-2'>Premium Vaporizer Authority</div><div class='text-sm text-gray-400'>Puffco has built dominant brand recognition in the concentrate and dab vaporizer space through consistent product launches and viral community content. Their name recognition generates branded search demand that lifts their organic visibility across the full category.</div></div><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>Dr. Dabber</div><div class='text-xs text-blue-400 mb-2'>DTC Competitor</div><div class='text-sm text-gray-400'>A strong direct-to-consumer vaporizer brand with consistent review site presence and community-driven content that ranks competitively on device and accessory queries.</div></div><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>Leafly / Reddit Communities</div><div class='text-xs text-blue-400 mb-2'>Editorial &amp; UGC Dominance</div><div class='text-sm text-gray-400'>Leafly's editorial authority and active Reddit communities dominate informational vaporizer queries, shaping buyer decisions before any brand page enters the conversation.</div></div></div><p class='text-gray-400 text-sm'>DIP Devices found traction in portable and desktop concentrate accessory queries — device-specific comparisons and technique content where community sites publish broadly but brands can win with product-specific depth.</p></div>"

focl_section = "<div class='competitor-section'><h3 class='text-xl font-bold text-white mb-4'>The Competitive Landscape</h3><div class='grid grid-cols-1 md:grid-cols-3 gap-4 mb-6'><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>Charlotte's Web</div><div class='text-xs text-blue-400 mb-2'>Category Authority</div><div class='text-sm text-gray-400'>The most recognized hemp CBD brand, Charlotte's Web holds deep domain authority built on years of educational content and press coverage across informational and commercial CBD queries.</div></div><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>Calm / Headspace</div><div class='text-xs text-blue-400 mb-2'>Wellness App Giants</div><div class='text-sm text-gray-400'>Dominate the wellness, stress, and sleep query landscape with massive content budgets and brand recognition that intercepts FOCL's target audience at the top of the funnel.</div></div><div class='rounded-xl p-4' style='background:#0a0f1e; border:1px solid #1f2937;'><div class='font-bold text-white mb-1'>cbdMD</div><div class='text-xs text-blue-400 mb-2'>SEO-Invested Competitor</div><div class='text-sm text-gray-400'>Aggressive keyword targeting across the full CBD spectrum with substantial content depth on benefit, dosage, and product queries that overlap directly with FOCL's audience.</div></div></div><p class='text-gray-400 text-sm'>FOCL's keyword opportunity is in premium wellness + CBD crossover content — functional performance, sleep, and recovery queries where pharma-grade competitors publish clinically and mass-market brands publish generically.</p></div>"

for slug, new_section in [('dip', dip_section), ('focl', focl_section)]:
    path = f'{base}/{slug}/index.html'
    html = open(path).read()
    # These are minimal - insert after the CTA section or at end of main content
    # Find the audit CTA section and insert before it
    cta_idx = html.lower().find('get your free seo audit')
    if cta_idx < 0:
        cta_idx = html.lower().find('free audit')
    if cta_idx > 0:
        # Find the enclosing div/section
        section_start = html.rfind('<section', 0, cta_idx)
        if section_start < 0:
            section_start = html.rfind('<div', 0, cta_idx)
        html = html[:section_start] + new_section + html[section_start:]
        open(path, 'w').write(html)
        print(f"Added to {slug}")
    else:
        print(f"CTA not found in {slug}")
