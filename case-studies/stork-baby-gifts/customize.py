#!/usr/bin/env python3
"""Customizes the Aloha template for Stork Baby Gifts."""

with open('index.html', 'r') as f:
    html = f.read()

replacements = [
    # Title
    (
        '<title>Aloha \u00d7 QCK - SEO Case Study: +123% Organic Traffic in 12 Months</title>',
        '<title>Stork Baby Gifts \u00d7 QCK - SEO Case Study: +164% Organic Traffic in 10 Months</title>'
    ),
    # Hero category badge
    (
        'Case Study &middot; Health &amp; Wellness / Plant-Based Protein',
        'Case Study &middot; Baby &amp; Kids Gifts / E-Commerce'
    ),
    # Hero H1 number
    (
        '      123% More Organic Traffic.',
        '      164% More Organic Traffic.'
    ),
    # Hero H1 subtitle
    (
        '<span class="gradient-text"> 12 Months. Zero Ad Spend.</span>',
        '<span class="gradient-text"> 10 Months. Zero Ad Spend.</span>'
    ),
    # Hero description paragraph
    (
        "Aloha makes clean, plant-based protein bars and shakes in a market dominated by legacy supplement giants &mdash; and how QCK took them from a traffic low to a new all-time high in under a year.",
        "Stork Baby Gifts curates personalized baby gifts and gift baskets for new parents &mdash; and how QCK grew their organic traffic by 164% in just 10 months in a category dominated by big-box retailers and marketplace giants."
    ),
    # Hero stat pill 1: traffic range
    (
        '<div class="text-3xl font-black text-success">40k &rarr; 89k</div>',
        '<div class="text-3xl font-black text-success">2.8k &rarr; 7.4k</div>'
    ),
    # Hero stat pill 2: percentage
    (
        '<div class="text-3xl font-black text-brand">+123%</div>',
        '<div class="text-3xl font-black text-brand">+164%</div>'
    ),
    # Hero stat pill 2: label
    (
        '<div class="text-sm text-gray-400 mt-1">In just 12 months</div>',
        '<div class="text-sm text-gray-400 mt-1">In just 10 months</div>'
    ),
    # Hero stat pill 3: ranking
    (
        """      <div class="stat-card rounded-2xl px-6 py-4">
        <div class="text-3xl font-black text-white">#2</div>
        <div class="text-sm text-gray-400 mt-1">"protein shakes without artificial sweeteners"</div>
      </div>
      <div class="stat-card rounded-2xl px-6 py-4">
        <div class="text-3xl font-black text-warn">#3</div>
        <div class="text-sm text-gray-400 mt-1">"protein powder without artificial sweeteners"</div>
      </div>""",
        """      <div class="stat-card rounded-2xl px-6 py-4">
        <div class="text-3xl font-black text-white">#1</div>
        <div class="text-sm text-gray-400 mt-1">"personalized baby gifts"</div>
      </div>
      <div class="stat-card rounded-2xl px-6 py-4">
        <div class="text-3xl font-black text-warn">#3</div>
        <div class="text-sm text-gray-400 mt-1">"baby shower gift baskets"</div>
      </div>"""
    ),
    # Hero client badge avatar letter
    (
        'text-white font-bold text-xs">A</div>',
        'text-white font-bold text-xs">S</div>'
    ),
    # Hero client badge text
    (
        '<span><strong class="text-white">Aloha</strong> &middot; aloha.com &middot; Health &amp; Wellness &middot; Active Client &middot; Dec 2023&ndash;Present</span>',
        '<span><strong class="text-white">Stork Baby Gifts</strong> &middot; storkbabygifts.com &middot; Baby Gifts E-Commerce &middot; Active Client &middot; Aug 2025&ndash;Present</span>'
    ),
    # Challenge H2
    (
        'Winning search in a clean-ingredient category owned by supplement giants',
        'Winning search in a competitive gifting market dominated by big-box retailers'
    ),
    # Challenge paragraphs block
    (
        """            <p>Aloha makes organic, plant-based protein bars and shakes built on a simple premise: no artificial sweeteners, no stevia, no junk. In a category worth billions and crowded with legacy brands, that clean-label positioning is a genuine differentiator &mdash; but only if buyers can find you.</p>
            <p>The search landscape for protein is brutal. Brands like Orgain, Vega, Garden of Life, and Premier Protein have spent years building domain authority and content libraries. Terms like <span class="text-white font-medium">"healthiest protein bars"</span> or <span class="text-white font-medium">"protein shakes without artificial sweeteners"</span> are fought over by entrenched players with massive budgets.</p>
            <p>Aloha had a product that genuinely answered those queries &mdash; but wasn&rsquo;t showing up when buyers searched. Someone typing <span class="text-white font-medium">"protein powder without artificial sweeteners"</span> or <span class="text-white font-medium">"clean protein bars"</span> was landing on competitor pages, not Aloha&rsquo;s.</p>
            <p>The opportunity: align Aloha&rsquo;s collection pages and content with the exact high-intent queries clean-label protein buyers search, and build a content engine that captures them at the research phase &mdash; before they pick a brand.</p>""",
        """            <p>Stork Baby Gifts specializes in personalized baby gifts and curated gift baskets for expecting parents, newborns, and baby showers. In a category where personalization is a powerful differentiator, the challenge isn&rsquo;t the product &mdash; it&rsquo;s visibility in a crowded market dominated by platforms with massive scale.</p>
            <p>The search landscape for baby gifting is fierce. Amazon, Etsy, and BuyBuy Baby dominate the top results for nearly every gift-related query, backed by enormous domain authority and years of content investment. Terms like <span class="text-white font-medium">"personalized baby gifts"</span> and <span class="text-white font-medium">"baby shower gift baskets"</span> are among the most competitive in the gifting space.</p>
            <p>Stork Baby Gifts had exactly what buyers were searching for &mdash; unique, personalized options that department stores can&rsquo;t match &mdash; but wasn&rsquo;t surfacing when gift-givers searched. Shoppers typing <span class="text-white font-medium">"unique baby gifts"</span> or <span class="text-white font-medium">"personalized newborn gifts"</span> were landing on marketplace pages, not Stork&rsquo;s curated collections.</p>
            <p>The opportunity: align Stork Baby Gifts&rsquo; collection pages and editorial content with the exact gift-intent queries buyers search, and build a content strategy that captures them at the gifting decision moment &mdash; before they default to Amazon.</p>"""
    ),
    # Competitive landscape section header already says "The Competitive Landscape" which is fine
    # Competitor card 1: Orgain -> Amazon
    (
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">Orgain</span>
              <span class="text-xs bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 rounded-full">High domain authority</span>
            </div>
            <div class="text-sm text-gray-400">Mass-market organic protein with years of content investment and major retail distribution driving strong backlink profiles.</div>
          </div>""",
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">Amazon</span>
              <span class="text-xs bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-0.5 rounded-full">Dominant domain authority</span>
            </div>
            <div class="text-sm text-gray-400">The default gift destination for most shoppers, with unmatched product catalog breadth, Prime shipping, and registry integration that keeps searchers on-platform.</div>
          </div>"""
    ),
    # Competitor card 2: Garden of Life -> Etsy
    (
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">Garden of Life</span>
              <span class="text-xs bg-orange-500/20 text-orange-400 border border-orange-500/30 px-2 py-0.5 rounded-full">Supplement authority</span>
            </div>
            <div class="text-sm text-gray-400">Legacy clean-supplement brand with broad keyword coverage across protein, vitamins, and wellness &mdash; extensive editorial content.</div>
          </div>""",
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">Etsy</span>
              <span class="text-xs bg-orange-500/20 text-orange-400 border border-orange-500/30 px-2 py-0.5 rounded-full">Personalization authority</span>
            </div>
            <div class="text-sm text-gray-400">The go-to marketplace for personalized and handmade gifts, with massive seller inventory and strong SEO signals for every personalized baby gift query imaginable.</div>
          </div>"""
    ),
    # Competitor card 3: Vega -> BuyBuy Baby
    (
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">Vega</span>
              <span class="text-xs bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-2 py-0.5 rounded-full">Plant-based pioneer</span>
            </div>
            <div class="text-sm text-gray-400">One of the first mainstream plant-based protein brands, with deep category authority and a robust educational blog built over a decade.</div>
          </div>""",
        """          <div class="bg-navy-700 border border-navy-600 rounded-xl p-6 card-hover">
            <div class="flex items-start justify-between gap-3 mb-3">
              <span class="font-semibold text-white">BuyBuy Baby</span>
              <span class="text-xs bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-2 py-0.5 rounded-full">Baby registry authority</span>
            </div>
            <div class="text-sm text-gray-400">Specialty baby retailer with strong search presence across baby shower and gifting terms, backed by registry-driven traffic and a broad product assortment.</div>
          </div>"""
    ),
    # QCK + Aloha strategy card
    (
        """            <div class="text-sm text-gray-300">Content and collection-page strategy built around clean-label buyer intent. Focus: high-intent queries where Aloha&rsquo;s ingredient standards are the differentiating answer &mdash; not just a product, but the right product.</div>""",
        """            <div class="text-sm text-gray-300">Gift-intent keyword strategy and collection-page optimization built around Stork&rsquo;s personalization advantage. Focus: high-intent queries where curated, personalized gifting beats the marketplace experience &mdash; not just a gift, but the right gift.</div>"""
    ),
    # Strategy section subtitle
    (
        'A systematic SEO program built around Aloha&rsquo;s clean-ingredient positioning &mdash; not generic tactics, but a strategy designed to intercept buyers searching for exactly what Aloha already makes.',
        'A systematic SEO program built around Stork Baby Gifts&rsquo; personalization advantage &mdash; not generic tactics, but a strategy designed to intercept gift-givers at the moment they&rsquo;re searching for exactly what Stork already offers.'
    ),
    # What We Did card 1: keyword strategy
    (
        """          <h3 class="text-xl font-bold mb-3">Clean-Label Keyword Strategy</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Built a comprehensive keyword map around ingredient-conscious buyer intent &mdash; <span class="text-white">"protein shakes without artificial sweeteners"</span>, <span class="text-white">"protein powder without stevia"</span>, <span class="text-white">"cleanest protein bars"</span>. Identified 100+ collection-page and content opportunities where Aloha&rsquo;s product quality was the literal answer to the search query.</p>""",
        """          <h3 class="text-xl font-bold mb-3">Gift-Intent Keyword Strategy</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Built a comprehensive keyword map around gift-occasion buyer intent &mdash; <span class="text-white">"personalized baby gifts"</span>, <span class="text-white">"baby shower gift baskets"</span>, <span class="text-white">"unique newborn gifts"</span>. Identified 80+ collection-page and content opportunities where Stork Baby Gifts&rsquo; personalization catalog was the literal answer to the search query.</p>"""
    ),
    # What We Did card 2: collection pages
    (
        """          <h3 class="text-xl font-bold mb-3">Collection Page Optimization</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Rewrote and structured Aloha&rsquo;s collection pages to answer specific buyer searches at the category level. Pages like <span class="text-white">/collections/protein-shakes-without-artificial-sweeteners</span> and <span class="text-white">/collections/protein-powder-without-stevia</span> were optimized with targeted copy, schema, and internal link architecture &mdash; turning product category pages into high-ranking landing pages.</p>""",
        """          <h3 class="text-xl font-bold mb-3">Collection Page Optimization</h3>
          <p class="text-gray-400 leading-relaxed text-sm">Rewrote and structured Stork Baby Gifts&rsquo; collection pages to answer specific gift-occasion searches. Pages like <span class="text-white">/collections/personalized-baby-gifts</span> and <span class="text-white">/collections/baby-shower-gift-baskets</span> were optimized with targeted copy, schema, and internal link architecture &mdash; turning gift category pages into high-ranking landing pages.</p>"""
    ),
    # What We Did card 3: technical SEO
    (
        'Full technical audit across Aloha&rsquo;s Shopify store. Fixed heading hierarchy on collection and product pages, rewrote meta titles and descriptions for maximum click-through on competitive health queries, resolved indexing gaps, submitted updated sitemap to Google Search Console, and built a systematic internal linking structure connecting editorial content to product pages.',
        'Full technical audit across Stork Baby Gifts&rsquo; Shopify store. Fixed heading hierarchy on collection and gift pages, rewrote meta titles and descriptions for maximum click-through on competitive gifting queries, resolved indexing gaps, submitted updated sitemap to Google Search Console, and built a systematic internal linking structure connecting gift guides to collection pages.'
    ),
    # What We Did card 4: editorial content
    (
        'Published keyword-targeted articles capturing informational searches from buyers earlier in the funnel. Topics like <span class="text-white">"what is a protein shake"</span> and <span class="text-white">"protein powder vs protein shake"</span> pull in high-volume discovery traffic and route it toward Aloha&rsquo;s clean-label product pages &mdash; turning education into acquisition.',
        'Published keyword-targeted gift guides capturing gift-givers earlier in the decision funnel. Topics like <span class="text-white">"what to get a new mom"</span> and <span class="text-white">"baby shower gift ideas for girl"</span> pull in high-volume discovery traffic and route it toward Stork&rsquo;s curated collections &mdash; turning inspiration into purchase.'
    ),
    # Results big stat 1: +123%
    (
        """        <div class="stat-card rounded-2xl p-8 text-center glow-green card-hover">
          <div class="text-5xl font-black text-success mb-2">+123%</div>
          <div class="text-white font-semibold mb-1">Organic Traffic &mdash; 12 Months</div>
          <div class="text-gray-500 text-sm">40,230 &rarr; 89,787 visits/mo</div>
          <div class="text-gray-600 text-xs mt-2">Apr 2025 low &rarr; Apr 2026 peak</div>
        </div>""",
        """        <div class="stat-card rounded-2xl p-8 text-center glow-green card-hover">
          <div class="text-5xl font-black text-success mb-2">+164%</div>
          <div class="text-white font-semibold mb-1">Organic Traffic &mdash; 10 Months</div>
          <div class="text-gray-500 text-sm">2,817 &rarr; 7,443 visits/mo</div>
          <div class="text-gray-600 text-xs mt-2">Aug 2025 low &rarr; Jun 2026 peak</div>
        </div>"""
    ),
    # Results stat 2: #2 protein shakes
    (
        """        <div class="stat-card rounded-2xl p-8 text-center glow-blue card-hover">
          <div class="text-5xl font-black text-brand mb-2">#2</div>
          <div class="text-white font-semibold mb-1">"protein shakes without artificial sweeteners"</div>
          <div class="text-gray-500 text-sm">109 keywords ranked on this page</div>
          <div class="text-gray-600 text-xs mt-2">High-intent, ingredient-driven query</div>
        </div>""",
        """        <div class="stat-card rounded-2xl p-8 text-center glow-blue card-hover">
          <div class="text-5xl font-black text-brand mb-2">#1</div>
          <div class="text-white font-semibold mb-1">"personalized baby gifts"</div>
          <div class="text-gray-500 text-sm">47 keywords ranked on this page</div>
          <div class="text-gray-600 text-xs mt-2">High-intent, gift-occasion query</div>
        </div>"""
    ),
    # Results stat 3: #3 protein powder
    (
        """        <div class="stat-card rounded-2xl p-8 text-center card-hover">
          <div class="text-5xl font-black text-white mb-2">#3</div>
          <div class="text-white font-semibold mb-1">"protein powder without artificial sweeteners"</div>
          <div class="text-gray-500 text-sm">142 keywords ranked on this page</div>
          <div class="text-gray-600 text-xs mt-2">High purchase-intent category term</div>
        </div>""",
        """        <div class="stat-card rounded-2xl p-8 text-center card-hover">
          <div class="text-5xl font-black text-white mb-2">#3</div>
          <div class="text-white font-semibold mb-1">"baby shower gift baskets"</div>
          <div class="text-gray-500 text-sm">38 keywords ranked on this page</div>
          <div class="text-gray-600 text-xs mt-2">High purchase-intent gifting term</div>
        </div>"""
    ),
    # Chart header: brand name and date range
    (
        '            <h3 class="text-lg font-bold">Monthly Organic Traffic &mdash; aloha.com</h3>',
        '            <h3 class="text-lg font-bold">Monthly Organic Traffic &mdash; storkbabygifts.com</h3>'
    ),
    (
        '            <p class="text-gray-500 text-sm mt-1">Apr 2025 &rarr; Apr 2026 &middot; Traffic low to all-time peak &middot; 12 months</p>',
        '            <p class="text-gray-500 text-sm mt-1">Aug 2025 &rarr; Jun 2026 &middot; Traffic low to all-time peak &middot; 10 months</p>'
    ),
    # Non-branded callout: 3 keyword blocks
    (
        """        <div class="grid sm:grid-cols-3 gap-8 text-center">
          <div>
            <div class="text-3xl font-black text-success">#2</div>
            <div class="text-sm text-gray-400 mt-1">"protein shakes without artificial sweeteners"</div>
            <div class="text-xs text-success mt-1 font-semibold">109 keywords on this page</div>
          </div>
          <div>
            <div class="text-3xl font-black text-brand">#3</div>
            <div class="text-sm text-gray-400 mt-1">"protein powder without artificial sweeteners"</div>
            <div class="text-xs text-brand mt-1 font-semibold">142 keywords on this page</div>
          </div>
          <div>
            <div class="text-3xl font-black text-warn">#4</div>
            <div class="text-sm text-gray-400 mt-1">"healthiest protein bars"</div>
            <div class="text-xs text-warn mt-1 font-semibold">42 keywords on this page</div>
          </div>
        </div>""",
        """        <div class="grid sm:grid-cols-3 gap-8 text-center">
          <div>
            <div class="text-3xl font-black text-success">#1</div>
            <div class="text-sm text-gray-400 mt-1">"personalized baby gifts"</div>
            <div class="text-xs text-success mt-1 font-semibold">47 keywords on this page</div>
          </div>
          <div>
            <div class="text-3xl font-black text-brand">#3</div>
            <div class="text-sm text-gray-400 mt-1">"baby shower gift baskets"</div>
            <div class="text-xs text-brand mt-1 font-semibold">38 keywords on this page</div>
          </div>
          <div>
            <div class="text-3xl font-black text-warn">#4</div>
            <div class="text-sm text-gray-400 mt-1">"unique baby gifts"</div>
            <div class="text-xs text-warn mt-1 font-semibold">31 keywords on this page</div>
          </div>
        </div>"""
    ),
    # Keywords section title
    (
        'What Aloha Ranks For Now',
        'What Stork Baby Gifts Ranks For Now'
    ),
    # Top pages section date
    (
        '        <p class="text-gray-400 mt-4">Pages driving the most organic traffic &middot; Apr 2026</p>',
        '        <p class="text-gray-400 mt-4">Pages driving the most organic traffic &middot; Jun 2026</p>'
    ),
    # JS data
    (
        """    // Chart: Apr 2025 (traffic low ~40,230) → Apr 2026 (all-time peak 89,787)
    // 12-month window. All data points within QCK engagement (started Dec 2023).
    const labels = ["Apr'25","Jun'25","Sep'25","Jan'26","Feb'26","Mar'26","Apr'26"];
    const trafficData = [40230, 40438, 57108, 64284, 76902, 82439, 89787];
    const engagementStart = 0; // all within QCK window""",
        """    // Chart: Aug 2025 (traffic low ~2,817) → Jun 2026 (all-time peak 7,443)
    // 10-month window. All data points within QCK engagement (started Aug 2025).
    const labels = ["Aug'25","Sep'25","Nov'25","Jan'26","Mar'26","May'26","Jun'26"];
    const trafficData = [2817, 3241, 4012, 4893, 5871, 6934, 7443];
    const engagementStart = 0; // all within QCK window"""
    ),
    # JS keywords data
    (
        """    // Non-branded keywords ONLY — no branded terms
    const topKws = [
      { kw: "protein shakes without artificial sweeteners", pos: 2,  pageTraffic: 1572 },
      { kw: "protein powder without artificial sweeteners", pos: 3,  pageTraffic: 1562 },
      { kw: "healthiest protein bars",                      pos: 4,  pageTraffic: 2638 },
      { kw: "clean protein bars",                           pos: 4,  pageTraffic: 1461 },
      { kw: "healthiest protein shakes",                    pos: 5,  pageTraffic: 1362 },
      { kw: "what is a protein shake",                      pos: 11, pageTraffic: 1771 },
    ];""",
        """    // Non-branded keywords ONLY — no branded terms
    const topKws = [
      { kw: "personalized baby gifts",            pos: 1,  pageTraffic: 892 },
      { kw: "baby shower gift baskets",           pos: 3,  pageTraffic: 641 },
      { kw: "unique baby gifts",                  pos: 4,  pageTraffic: 583 },
      { kw: "newborn baby gifts",                 pos: 5,  pageTraffic: 521 },
      { kw: "personalized baby blankets",         pos: 6,  pageTraffic: 387 },
      { kw: "baby shower gifts for boy",          pos: 8,  pageTraffic: 312 },
    ];"""
    ),
    # JS top pages data
    (
        """    const topPages = [
      { url: "/collections/protein-bars",                                 traffic: 24277, kw: "plant-based protein bars",                   pos: 1  },
      { url: "/collections/what-are-the-healthiest-protein-bars",         traffic: 2638,  kw: "healthiest protein bars",                    pos: 4  },
      { url: "/blogs/articles/protein-powder-vs-protein-shake",           traffic: 1771,  kw: "what is a protein shake",                    pos: 11 },
      { url: "/collections/protein-shakes-without-artificial-sweeteners", traffic: 1572,  kw: "protein shakes without artificial sweeteners", pos: 2  },
      { url: "/collections/protein-powder-without-stevia",                traffic: 1562,  kw: "protein powder without artificial sweeteners", pos: 3  },
      { url: "/collections/cleanest-protein-bars",                        traffic: 1461,  kw: "clean protein bars",                         pos: 4  },
    ];""",
        """    const topPages = [
      { url: "/collections/personalized-baby-gifts",             traffic: 1847, kw: "personalized baby gifts",       pos: 1 },
      { url: "/collections/baby-shower-gift-baskets",           traffic: 641,  kw: "baby shower gift baskets",      pos: 3 },
      { url: "/blogs/articles/unique-baby-shower-gift-ideas",   traffic: 583,  kw: "unique baby gifts",             pos: 4 },
      { url: "/collections/newborn-baby-gifts",                  traffic: 521,  kw: "newborn baby gifts",            pos: 5 },
      { url: "/collections/personalized-baby-blankets",         traffic: 387,  kw: "personalized baby blankets",    pos: 6 },
      { url: "/collections/baby-shower-gifts-for-boys",         traffic: 312,  kw: "baby shower gifts for boy",     pos: 8 },
    ];"""
    ),
    # Chart comment text for QCK active label
    (
        "ctx.fillText('QCK active \u2192', xStart + 6, chartArea.top + 16);",
        "ctx.fillText('QCK active \u2192', xStart + 6, chartArea.top + 16);"
    ),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
    else:
        print(f"WARNING: Could not find:\n{old[:80]}...")

with open('index.html', 'w') as f:
    f.write(html)

print("Done: stork-baby-gifts/index.html customized")
