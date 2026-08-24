"""
Vercel Serverless Function (Python) — /api/generate-report
POST { "domain": "aloha.com" }
→ Pulls Ahrefs data, generates HTML report, deploys to Vercel, returns { "url": "...", "slug": "..." }
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import requests
import hashlib
import time
import re
from datetime import date, timedelta

AHREFS_TOKEN = os.environ.get("AHREFS_API_TOKEN", "")
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "")
VERCEL_PROJECT_ID = os.environ.get("VERCEL_PROJECT_ID", "prj_D6ly9Z60hiJFBPCi2AaH2G1lTROS")
AHREFS_BASE = "https://api.ahrefs.com/v3"
TODAY = date.today().strftime("%Y-%m-%d")
YESTERDAY = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

def ahrefs_get(path, params):
    try:
        r = requests.get(f"{AHREFS_BASE}{path}",
            headers={"Authorization": f"Bearer {AHREFS_TOKEN}"},
            params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

def pull_domain_data(domain):
    data = {}
    dr_data = ahrefs_get("/site-explorer/domain-rating", {"target": domain, "date": YESTERDAY})
    time.sleep(0.45)
    if dr_data:
        data["domain_rating"] = dr_data.get("domain_rating", {}).get("domain_rating", 0)
        data["ahrefs_rank"] = dr_data.get("domain_rating", {}).get("ahrefs_rank", 0)

    metrics = ahrefs_get("/site-explorer/metrics", {"target": domain, "date": YESTERDAY, "mode": "domain", "country": "us"})
    time.sleep(0.45)
    if metrics:
        m = metrics.get("metrics", {})
        data["org_traffic"] = m.get("org_traffic", 0)
        data["org_keywords"] = m.get("org_keywords", 0)
        data["org_keywords_1_3"] = m.get("org_keywords_1_3", 0)

    top_pages = ahrefs_get("/site-explorer/top-pages", {
        "target": domain, "date": YESTERDAY, "mode": "domain",
        "select": "raw_url,keywords,top_keyword_best_position,top_keyword_best_position_title", "limit": 10
    })
    time.sleep(0.45)
    data["top_pages"] = top_pages.get("pages", []) if top_pages else []

    org_kws = ahrefs_get("/site-explorer/organic-keywords", {
        "target": domain, "date": YESTERDAY,
        "select": "keyword,volume,cpc,best_position_set", "limit": 20, "mode": "domain"
    })
    time.sleep(0.45)
    data["top_keywords"] = org_kws.get("keywords", []) if org_kws else []

    return data

def classify_dr(dr):
    if dr >= 60:
        return "high", "70/30", 70, 30
    elif dr >= 30:
        return "mid", "60/40", 60, 40
    else:
        return "low", "50/50", 50, 50

def format_num(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)

def generate_html(domain, data):
    dr = data.get("domain_rating", 0)
    traffic = data.get("org_traffic", 0)
    keywords = data.get("org_keywords", 0)
    top_kws_1_3 = data.get("org_keywords_1_3", 0)
    top_pages = data.get("top_pages", [])
    top_kws = data.get("top_keywords", [])

    dr_tier, split_label, col_pct, blog_pct = classify_dr(dr)
    traffic_3x = format_num(traffic * 3)
    traffic_7x = format_num(traffic * 7)
    traffic_fmt = format_num(traffic)
    kw_fmt = format_num(keywords)

    # Build top pages rows
    pages_rows = ""
    for p in top_pages[:8]:
        url = p.get("raw_url", "")
        kws = p.get("keywords", 0)
        pos = p.get("top_keyword_best_position", "")
        title = p.get("top_keyword_best_position_title", "")
        page_type = "Blog" if "/blog" in url else "Collection" if "/collection" in url else "Product" if "/product" in url else "Page"
        tag_class = "tag-blog" if page_type == "Blog" else "tag-collection" if page_type == "Collection" else "tag-product"
        pages_rows += f'<li><a class="page-url" href="{url}" target="_blank">{url.replace("https://","").replace("http://","")[:60]}</a><div class="page-meta"><span class="page-type-tag {tag_class}">{page_type}</span><span class="page-kws">{kws} kws · Pos #{pos}</span></div></li>\n'

    # Build keyword chips
    kw_chips = ""
    for kw in top_kws[:12]:
        vol = kw.get("volume", 0)
        cpc = kw.get("cpc") or 0
        word = kw.get("keyword", "")
        if cpc >= 30:
            diff, dc = "HIGH", "diff-high"
        elif cpc >= 10:
            diff, dc = "MED", "diff-med"
        else:
            diff, dc = "LOW", "diff-low"
        kw_chips += f'<span class="kw-chip"><span class="kw-vol">{format_num(vol)}</span> {word} <span class="kw-diff {dc}">{diff}</span></span>\n'

    created_date = date.today().strftime("%b %d, %Y")
    domain_display = domain.replace("www.", "")

    # Read the aloha template and adapt it
    template_path = os.path.join(os.path.dirname(__file__), "..", "intro", "aloha-seo-demand-analysis.html")
    with open(template_path, "r") as f:
        html = f.read()

    # Replace aloha-specific data with real domain data
    replacements = {
        "aloha.com": domain_display,
        "aloha-seo-demand-analysis": f"{domain_display.replace('.', '-')}-seo-demand-analysis",
        "SEO Demand Analysis — aloha.com": f"SEO Demand Analysis — {domain_display}",
        "Generated Aug 24, 2026": f"Generated {created_date}",
        "58,339": f"{traffic:,}",
        "4,869": f"{keywords:,}",
        "69": str(int(dr)),
        "1,554": f"{top_kws_1_3:,}",
        "32% in positions 1–3": f"{int(top_kws_1_3/max(keywords,1)*100)}% in positions 1–3" if keywords > 0 else "—",
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    return html

def deploy_html(domain, html_content):
    slug = domain.replace(".", "-") + "-seo-demand-analysis"
    file_path = f"intro/{slug}.html"
    content_bytes = html_content.encode("utf-8")
    sha1 = hashlib.sha1(content_bytes).hexdigest()

    # Upload file
    r1 = requests.post("https://api.vercel.com/v2/files",
        headers={"Authorization": f"Bearer {VERCEL_TOKEN}", "x-vercel-digest": sha1, "Content-Type": "text/html"},
        data=content_bytes)

    if r1.status_code not in (200, 409):
        return None, f"File upload failed: {r1.status_code}"

    # Deploy
    r2 = requests.post("https://api.vercel.com/v13/deployments",
        headers={"Authorization": f"Bearer {VERCEL_TOKEN}", "Content-Type": "application/json"},
        json={"name": "qck-case-studies", "project": VERCEL_PROJECT_ID,
              "files": [{"file": file_path, "sha": sha1, "size": len(content_bytes)}],
              "projectSettings": {"outputDirectory": "."}, "target": "production"})

    d = r2.json()
    deploy_id = d.get("id", "")
    preview_url = d.get("url", "")

    if not deploy_id:
        return None, f"Deploy failed: {d}"

    # Wait for ready
    for _ in range(20):
        time.sleep(4)
        state = requests.get(f"https://api.vercel.com/v13/deployments/{deploy_id}",
            headers={"Authorization": f"Bearer {VERCEL_TOKEN}"}).json().get("readyState", "")
        if state == "READY":
            break

    # Assign alias
    requests.post(f"https://api.vercel.com/v2/deployments/{preview_url}/aliases",
        headers={"Authorization": f"Bearer {VERCEL_TOKEN}", "Content-Type": "application/json"},
        json={"alias": "cs.qck.co"})

    live_url = f"https://cs.qck.co/intro/{slug}"
    return live_url, None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/api/generate-report":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        domain = body.get("domain", "").strip().lower()
        domain = re.sub(r"^https?://", "", domain).replace("www.", "").split("/")[0]

        if not domain:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "domain required"}).encode())
            return

        try:
            # Pull data
            data = pull_domain_data(domain)

            # Generate HTML
            html = generate_html(domain, data)

            # Deploy
            live_url, err = deploy_html(domain, html)
            if err:
                raise Exception(err)

            slug = domain.replace(".", "-") + "-seo-demand-analysis"
            result = {
                "ok": True,
                "domain": domain,
                "url": live_url,
                "slug": slug,
                "dr": data.get("domain_rating", 0),
                "traffic": data.get("org_traffic", 0),
                "keywords": data.get("org_keywords", 0),
            }
        except Exception as e:
            result = {"ok": False, "error": str(e)}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
