// Vercel Serverless Function — /api/generate-report
// POST { "domain": "aloha.com" } (accepts any format: https://www.aloha.com/, aloha.com, etc.)
// → Pulls Ahrefs data, generates HTML report, deploys to cs.qck.co, returns { ok, url, dr, traffic, keywords }

const https = require('https');
const crypto = require('crypto');

const AHREFS_TOKEN = process.env.AHREFS_API_TOKEN || '';
const VERCEL_TOKEN = process.env.VERCEL_TOKEN || '';
const PROJECT_ID = process.env.VERCEL_PROJECT_ID || 'prj_D6ly9Z60hiJFBPCi2AaH2G1lTROS';

// ── helpers ──────────────────────────────────────────────────────────────────

function cleanDomain(raw) {
  return raw
    .trim()
    .toLowerCase()
    .replace(/^https?:\/\//, '')
    .replace(/^www\./, '')
    .split('/')[0]
    .split('?')[0];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function formatNum(n) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${Math.round(n / 1_000)}K`;
  return String(n);
}

function httpJson(url, options = {}, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, res => {
      let data = '';
      res.on('data', chunk => (data += chunk));
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(data) }); }
        catch { resolve({ status: res.statusCode, body: data }); }
      });
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('timeout')); });
    if (body) req.write(typeof body === 'string' ? body : JSON.stringify(body));
    req.end();
  });
}

function ahrefsGet(path, params) {
  const qs = new URLSearchParams(params).toString();
  const url = `https://api.ahrefs.com/v3${path}?${qs}`;
  return httpJson(url, {
    method: 'GET',
    headers: { Authorization: `Bearer ${AHREFS_TOKEN}` }
  });
}

// ── Ahrefs data pull ──────────────────────────────────────────────────────────

async function pullDomainData(domain) {
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const data = { domain_rating: 0, ahrefs_rank: 0, org_traffic: 0, org_keywords: 0, org_keywords_1_3: 0, top_pages: [], top_keywords: [] };

  // Domain Rating
  const dr = await ahrefsGet('/site-explorer/domain-rating', { target: domain, date: yesterday });
  if (dr.status === 200 && dr.body.domain_rating) {
    data.domain_rating = dr.body.domain_rating.domain_rating || 0;
    data.ahrefs_rank = dr.body.domain_rating.ahrefs_rank || 0;
  }
  await sleep(500);

  // Metrics
  const metrics = await ahrefsGet('/site-explorer/metrics', { target: domain, date: yesterday, mode: 'domain', country: 'us' });
  if (metrics.status === 200 && metrics.body.metrics) {
    const m = metrics.body.metrics;
    data.org_traffic = m.org_traffic || 0;
    data.org_keywords = m.org_keywords || 0;
    data.org_keywords_1_3 = m.org_keywords_1_3 || 0;
  }
  await sleep(500);

  // Top pages
  const pages = await ahrefsGet('/site-explorer/top-pages', {
    target: domain, date: yesterday, mode: 'domain',
    select: 'raw_url,keywords,top_keyword_best_position,top_keyword_best_position_title', limit: 10
  });
  if (pages.status === 200 && pages.body.pages) data.top_pages = pages.body.pages;
  await sleep(500);

  // Organic keywords
  const kws = await ahrefsGet('/site-explorer/organic-keywords', {
    target: domain, date: yesterday,
    select: 'keyword,volume,cpc,best_position_set', limit: 20, mode: 'domain'
  });
  if (kws.status === 200 && kws.body.keywords) data.top_keywords = kws.body.keywords;

  return data;
}

// ── HTML generation ───────────────────────────────────────────────────────────

function buildTopPagesRows(pages) {
  return pages.slice(0, 8).map(p => {
    const url = p.raw_url || '';
    const kws = p.keywords || 0;
    const pos = p.top_keyword_best_position || '';
    const short = url.replace(/^https?:\/\//, '').slice(0, 65);
    const type = url.includes('/blog') ? 'Blog' : url.includes('/collection') ? 'Collection' : url.includes('/product') ? 'Product' : 'Page';
    const cls = type === 'Blog' ? 'tag-blog' : type === 'Collection' ? 'tag-collection' : 'tag-product';
    return `<li><a class="page-url" href="${url}" target="_blank">${short}</a><div class="page-meta"><span class="page-type-tag ${cls}">${type}</span><span class="page-kws">${kws} kws${pos ? ` · Pos #${pos}` : ''}</span></div></li>`;
  }).join('\n');
}

function buildKwChips(kws) {
  return kws.slice(0, 12).map(kw => {
    const vol = kw.volume || 0;
    const cpc = kw.cpc || 0;
    const word = kw.keyword || '';
    const [diff, cls] = cpc >= 30 ? ['HIGH', 'diff-high'] : cpc >= 10 ? ['MED', 'diff-med'] : ['LOW', 'diff-low'];
    return `<span class="kw-chip"><span class="kw-vol">${formatNum(vol)}</span> ${word} <span class="kw-diff ${cls}">${diff}</span></span>`;
  }).join('\n');
}

function classifyDr(dr) {
  if (dr >= 60) return { tier: 'high', colPct: 70, blogPct: 30 };
  if (dr >= 30) return { tier: 'mid', colPct: 60, blogPct: 40 };
  return { tier: 'low', colPct: 50, blogPct: 50 };
}

function generateHtml(domain, data, alohaTemplate) {
  const dr = Math.round(data.domain_rating || 0);
  const traffic = data.org_traffic || 0;
  const keywords = data.org_keywords || 0;
  const top13 = data.org_keywords_1_3 || 0;
  const { colPct, blogPct } = classifyDr(dr);

  const created = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const domainDisplay = domain.replace('www.', '');
  const pct13 = keywords > 0 ? `${Math.round(top13 / keywords * 100)}% in positions 1–3` : '—';

  const pagesRows = buildTopPagesRows(data.top_pages);
  const kwChips = buildKwChips(data.top_keywords);

  // Start from the aloha template and do targeted replacements
  let html = alohaTemplate;

  // Header replacements
  html = html.replace(/SEO Demand Analysis — aloha\.com/g, `SEO Demand Analysis — ${domainDisplay}`);
  html = html.replace(/<strong>aloha\.com<\/strong>/g, `<strong>${domainDisplay}</strong>`);
  html = html.replace(/Generated Aug 24, 2026/g, `Generated ${created}`);

  // Metric bar badges
  html = html.replace(/<span class="badge-value">69<\/span>/g, `<span class="badge-value">${dr}</span>`);
  html = html.replace(/<span class="badge-value">58,339<\/span>/g, `<span class="badge-value">${traffic.toLocaleString()}</span>`);
  html = html.replace(/<span class="badge-value">4,869<\/span>/g, `<span class="badge-value">${keywords.toLocaleString()}</span>`);

  // Stat cards in metric bar
  html = html.replace(/>69</g, `>${dr}<`);
  html = html.replace(/58,339/g, traffic.toLocaleString());
  html = html.replace(/4,869/g, keywords.toLocaleString());
  html = html.replace(/1,554/g, top13.toLocaleString());
  html = html.replace(/32% in positions 1–3/g, pct13);

  // Domain references
  html = html.replace(/aloha\.com/g, domainDisplay);
  html = html.replace(/aloha-seo-demand-analysis/g, `${domainDisplay.replace(/\./g, '-')}-seo-demand-analysis`);

  // Aloha top pages — replace the hardcoded list with real data
  const alohaPagesSectionStart = html.indexOf('<!-- Aloha top pages -->');
  // Use a placeholder approach — inject real pages into Aloha's own expand section
  if (pagesRows) {
    html = html.replace(
      /(<tr class="comp-detail-row" id="detail-aloha">[\s\S]*?<ul class="comp-pages-list">)([\s\S]*?)(<\/ul>)/m,
      (match, before, _old, after) => {
        if (pagesRows.trim()) return `${before}\n${pagesRows}\n${after}`;
        return match;
      }
    );
  }

  // Content split — update percentages
  html = html.replace(
    /(<div class="split-col collections" style="width:)70(%">)70(% Collections)/,
    `$1${colPct}$2${colPct}% Collections`
  );
  html = html.replace(
    /(<div class="split-col blogs" style="width:)30(%">)30(% Blogs)/,
    `$1${blogPct}$2${blogPct}% Blogs`
  );

  // TAM numbers
  const t3x = formatNum(traffic * 3);
  const t7x = formatNum(traffic * 7);
  html = html.replace(/175K/g, t3x);
  html = html.replace(/380K\+/g, t7x + '+');

  // Footer date
  html = html.replace(/Generated Aug 24, 2026/g, `Generated ${created}`);

  return html;
}

// ── Vercel deploy ─────────────────────────────────────────────────────────────

async function deployHtml(domain, htmlContent) {
  const slug = `${domain.replace(/\./g, '-')}-seo-demand-analysis`;
  const filePath = `intro/${slug}.html`;
  const buf = Buffer.from(htmlContent, 'utf8');
  const sha1 = crypto.createHash('sha1').update(buf).digest('hex');

  // Upload file
  const upload = await httpJson(`https://api.vercel.com/v2/files`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'x-vercel-digest': sha1, 'Content-Type': 'text/html', 'Content-Length': buf.length }
  }, buf.toString());

  // Deploy
  const deployBody = JSON.stringify({
    name: 'qck-case-studies', project: PROJECT_ID,
    files: [{ file: filePath, sha: sha1, size: buf.length }],
    projectSettings: { outputDirectory: '.' },
    target: 'production'
  });

  const deploy = await httpJson('https://api.vercel.com/v13/deployments', {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(deployBody) }
  }, deployBody);

  const deployId = deploy.body.id;
  const previewUrl = deploy.body.url;
  if (!deployId) throw new Error(`Deploy failed: ${JSON.stringify(deploy.body)}`);

  // Wait for READY
  for (let i = 0; i < 20; i++) {
    await sleep(4000);
    const status = await httpJson(`https://api.vercel.com/v13/deployments/${deployId}`, {
      method: 'GET', headers: { Authorization: `Bearer ${VERCEL_TOKEN}` }
    });
    if (status.body.readyState === 'READY') break;
  }

  // Assign cs.qck.co alias
  const aliasBody = JSON.stringify({ alias: 'cs.qck.co' });
  await httpJson(`https://api.vercel.com/v2/deployments/${previewUrl}/aliases`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(aliasBody) }
  }, aliasBody);

  return `https://cs.qck.co/intro/${slug}`;
}

// ── Handler ───────────────────────────────────────────────────────────────────

const fs = require('fs');
const path = require('path');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  let body = '';
  for await (const chunk of req) body += chunk;

  let parsed;
  try { parsed = JSON.parse(body); }
  catch { return res.status(400).json({ error: 'Invalid JSON body' }); }

  const rawDomain = parsed.domain || '';
  const domain = cleanDomain(rawDomain);
  if (!domain || !domain.includes('.')) {
    return res.status(400).json({ error: 'Invalid domain. Example: edisonbicycles.com' });
  }

  try {
    // Pull Ahrefs data
    const data = await pullDomainData(domain);

    // Load aloha template as base
    const templatePath = path.join(process.cwd(), 'intro', 'aloha-seo-demand-analysis.html');
    let template;
    try {
      template = fs.readFileSync(templatePath, 'utf8');
    } catch {
      // Fallback: fetch from live URL
      const r = await httpJson('https://cs.qck.co/intro/aloha-seo-demand-analysis', { method: 'GET', headers: { 'Accept': 'text/html' } });
      template = typeof r.body === 'string' ? r.body : '';
    }

    // Generate HTML
    const html = generateHtml(domain, data, template);

    // Deploy
    const liveUrl = await deployHtml(domain, html);

    return res.status(200).json({
      ok: true,
      domain,
      url: liveUrl,
      slug: `${domain.replace(/\./g, '-')}-seo-demand-analysis`,
      dr: data.domain_rating,
      traffic: data.org_traffic,
      keywords: data.org_keywords
    });

  } catch (err) {
    console.error('generate-report error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
};
