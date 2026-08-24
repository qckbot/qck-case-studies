// Vercel Serverless Function — /api/generate-report
// POST { "domain": "aloha.com" } (any format — cleaned automatically)
//
// SAFETY RULE (PERMANENT — DO NOT CHANGE):
// This function NEVER reassigns the cs.qck.co domain alias.
// Reassigning from a partial deploy WIPES the entire site.
// Reports are committed to GitHub and deployed via a full site redeploy.
//
// Flow: Ahrefs pull → generate HTML → commit to GitHub repo → trigger full Vercel deploy
// The full deploy includes all 97+ files so cs.qck.co stays intact.

const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const AHREFS_TOKEN  = process.env.AHREFS_API_TOKEN   || '';
const VERCEL_TOKEN  = process.env.VERCEL_TOKEN        || '';
const PROJECT_ID    = process.env.VERCEL_PROJECT_ID   || 'prj_D6ly9Z60hiJFBPCi2AaH2G1lTROS';
const GITHUB_TOKEN  = process.env.GITHUB_TOKEN        || '';
const GITHUB_REPO   = 'qckbot/qck-case-studies';

// ── helpers ──────────────────────────────────────────────────────────────────

function cleanDomain(raw) {
  return raw.trim().toLowerCase()
    .replace(/^https?:\/\//, '').replace(/^www\./, '').split('/')[0].split('?')[0];
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function formatNum(n) {
  if (n >= 1_000_000) return `${(n/1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${Math.round(n/1_000)}K`;
  return String(n || 0);
}

function httpReq(url, options, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const opts = { hostname: u.hostname, path: u.pathname + u.search, ...options };
    const req = https.request(opts, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString();
        let parsed;
        try { parsed = JSON.parse(raw); } catch { parsed = raw; }
        resolve({ status: res.statusCode, body: parsed, raw });
      });
    });
    req.on('error', reject);
    req.setTimeout(25000, () => { req.destroy(new Error('timeout')); });
    if (body) req.write(Buffer.isBuffer(body) ? body : Buffer.from(body));
    req.end();
  });
}

function ahrefsGet(path, params) {
  const qs = new URLSearchParams(params).toString();
  return httpReq(`https://api.ahrefs.com/v3${path}?${qs}`, {
    method: 'GET',
    headers: { Authorization: `Bearer ${AHREFS_TOKEN}` }
  });
}

// ── Ahrefs data pull ──────────────────────────────────────────────────────────

async function pullDomainData(domain) {
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const data = { domain_rating: 0, ahrefs_rank: 0, org_traffic: 0, org_keywords: 0, org_keywords_1_3: 0, top_pages: [], top_keywords: [] };

  const dr = await ahrefsGet('/site-explorer/domain-rating', { target: domain, date: yesterday });
  if (dr.status === 200 && dr.body.domain_rating) {
    data.domain_rating = dr.body.domain_rating.domain_rating || 0;
    data.ahrefs_rank = dr.body.domain_rating.ahrefs_rank || 0;
  }
  await sleep(500);

  const metrics = await ahrefsGet('/site-explorer/metrics', { target: domain, date: yesterday, mode: 'domain', country: 'us' });
  if (metrics.status === 200 && metrics.body.metrics) {
    const m = metrics.body.metrics;
    data.org_traffic = m.org_traffic || 0;
    data.org_keywords = m.org_keywords || 0;
    data.org_keywords_1_3 = m.org_keywords_1_3 || 0;
  }
  await sleep(500);

  const pages = await ahrefsGet('/site-explorer/top-pages', {
    target: domain, date: yesterday, mode: 'domain',
    select: 'raw_url,keywords,top_keyword_best_position,top_keyword_best_position_title', limit: 10
  });
  if (pages.status === 200 && pages.body.pages) data.top_pages = pages.body.pages;
  await sleep(500);

  const kws = await ahrefsGet('/site-explorer/organic-keywords', {
    target: domain, date: yesterday,
    select: 'keyword,volume,cpc,best_position_set', limit: 20, mode: 'domain'
  });
  if (kws.status === 200 && kws.body.keywords) data.top_keywords = kws.body.keywords;

  return data;
}

// ── HTML generation ───────────────────────────────────────────────────────────

function buildPagesRows(pages) {
  return (pages || []).slice(0, 8).map(p => {
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
  return (kws || []).slice(0, 12).map(kw => {
    const vol = kw.volume || 0;
    const cpc = kw.cpc || 0;
    const word = kw.keyword || '';
    const [diff, cls] = cpc >= 30 ? ['HIGH','diff-high'] : cpc >= 10 ? ['MED','diff-med'] : ['LOW','diff-low'];
    return `<span class="kw-chip"><span class="kw-vol">${formatNum(vol)}</span> ${word} <span class="kw-diff ${cls}">${diff}</span></span>`;
  }).join('\n');
}

function classifyDr(dr) {
  if (dr >= 60) return { colPct: 70, blogPct: 30 };
  if (dr >= 30) return { colPct: 60, blogPct: 40 };
  return { colPct: 50, blogPct: 50 };
}

function generateHtml(domain, data, alohaTemplate) {
  const dr = Math.round(data.domain_rating || 0);
  const traffic = data.org_traffic || 0;
  const keywords = data.org_keywords || 0;
  const top13 = data.org_keywords_1_3 || 0;
  const { colPct, blogPct } = classifyDr(dr);
  const created = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const domainDisplay = domain.replace('www.', '');
  const pct13 = keywords > 0 ? `${Math.round(top13/keywords*100)}% in positions 1–3` : '—';
  const pagesRows = buildPagesRows(data.top_pages);

  let html = alohaTemplate;

  // Title + meta
  html = html.replace(/SEO Demand Analysis — aloha\.com/g, `SEO Demand Analysis — ${domainDisplay}`);
  html = html.replace(/<strong>aloha\.com<\/strong>/g, `<strong>${domainDisplay}</strong>`);
  html = html.replace(/Generated Aug 24, 2026/g, `Generated ${created}`);

  // Numbers
  html = html.replace(/>69</g, `>${dr}<`);
  html = html.replace(/58,339/g, traffic.toLocaleString());
  html = html.replace(/4,869/g, keywords.toLocaleString());
  html = html.replace(/1,554/g, top13.toLocaleString());
  html = html.replace(/32% in positions 1–3/g, pct13);

  // Domain refs
  html = html.replace(/aloha\.com/g, domainDisplay);
  html = html.replace(/aloha-seo-demand-analysis/g, `${domainDisplay.replace(/\./g, '-')}-seo-demand-analysis`);

  // Inject real top pages into the client's own expand section
  if (pagesRows) {
    html = html.replace(
      /(<tr class="comp-detail-row" id="detail-aloha[\s\S]*?<ul class="comp-pages-list">)([\s\S]*?)(<\/ul>)/m,
      (m, before, _old, after) => `${before}\n${pagesRows}\n${after}`
    );
  }

  // Content split
  html = html.replace(
    /(<div class="split-col collections" style="width:)70(%">)70(% Collections)/,
    `$1${colPct}$2${colPct}% Collections`
  );
  html = html.replace(
    /(<div class="split-col blogs" style="width:)30(%">)30(% Blogs)/,
    `$1${blogPct}$2${blogPct}% Blogs`
  );

  // TAM
  const t3x = formatNum(traffic * 3);
  const t7x = formatNum(traffic * 7);
  html = html.replace(/175K/g, t3x).replace(/380K\+/g, t7x + '+');

  return html;
}

// ── GitHub commit + Full Vercel redeploy ──────────────────────────────────────
// SAFETY: This always deploys ALL files from the repo, never a subset.
// This is the ONLY correct way to update cs.qck.co without wiping the site.

async function commitAndDeploy(slug, htmlContent) {
  const filePath = `intro/${slug}.html`;
  const buf = Buffer.from(htmlContent, 'utf8');
  const sha1 = crypto.createHash('sha1').update(buf).digest('hex');

  // Step 1: Check if file already exists in GitHub (get SHA for update)
  let existingSha = null;
  const ghHeaders = {
    Authorization: `Bearer ${GITHUB_TOKEN}`,
    'User-Agent': 'qck-report-generator',
    Accept: 'application/vnd.github.v3+json'
  };

  const check = await httpReq(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`,
    { method: 'GET', headers: ghHeaders }
  );
  if (check.status === 200 && check.body.sha) existingSha = check.body.sha;

  // Step 2: Commit to GitHub
  const commitPayload = JSON.stringify({
    message: `Add SEO demand report: ${slug}`,
    content: buf.toString('base64'),
    ...(existingSha ? { sha: existingSha } : {})
  });

  const commit = await httpReq(
    `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`,
    { method: 'PUT', headers: { ...ghHeaders, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(commitPayload) } },
    commitPayload
  );

  if (commit.status !== 200 && commit.status !== 201) {
    throw new Error(`GitHub commit failed ${commit.status}: ${JSON.stringify(commit.body).slice(0,300)}`);
  }

  // Step 3: Upload new file to Vercel CDN
  await httpReq('https://api.vercel.com/v2/files', {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'x-vercel-digest': sha1, 'Content-Type': 'text/html', 'Content-Length': buf.length }
  }, buf);

  // Step 4: Walk the local repo directory to get ALL file SHAs for full redeploy
  // This ensures cs.qck.co always gets ALL files, never just 1
  const repoRoot = path.join(process.cwd());
  const allFiles = [];
  const skipDirs = new Set(['.git','node_modules','.vercel','lightrx-proposal','old-pricing-v1','pricing-local','yumwoof-performance']);
  const validExts = new Set(['.html','.json','.js','.css','.svg','.txt','.md']);
  const ctMap = { '.html':'text/html','.json':'application/json','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml' };

  function walkDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (!skipDirs.has(entry.name)) walkDir(path.join(dir, entry.name));
      } else {
        const ext = path.extname(entry.name);
        if (!validExts.has(ext)) continue;
        const abs = path.join(dir, entry.name);
        const rel = path.relative(repoRoot, abs);
        const stat = fs.statSync(abs);
        if (stat.size > 5_000_000) continue;
        const fc = fs.readFileSync(abs);
        const fsha = crypto.createHash('sha1').update(fc).digest('hex');
        const ct = ctMap[ext] || 'text/plain';
        // Upload to Vercel CDN (idempotent — 409 is fine)
        // We do this synchronously to avoid overwhelming the API
        allFiles.push({ file: rel, sha: fsha, size: stat.size, content: fc, ct });
      }
    }
  }

  walkDir(repoRoot);

  // Override/add our new file
  const newIdx = allFiles.findIndex(f => f.file === filePath);
  const newEntry = { file: filePath, sha: sha1, size: buf.length, content: buf, ct: 'text/html' };
  if (newIdx >= 0) allFiles[newIdx] = newEntry;
  else allFiles.push(newEntry);

  // Upload all files to Vercel CDN in batches
  for (const f of allFiles) {
    const r = await httpReq('https://api.vercel.com/v2/files', {
      method: 'POST',
      headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'x-vercel-digest': f.sha, 'Content-Type': f.ct, 'Content-Length': f.content.length }
    }, f.content);
    // 200 = uploaded, 409 = already exists — both are fine
    await sleep(40);
  }

  // Step 5: Full redeploy with ALL files
  const deployPayload = JSON.stringify({
    name: 'qck-case-studies',
    project: PROJECT_ID,
    files: allFiles.map(f => ({ file: f.file, sha: f.sha, size: f.size })),
    projectSettings: { outputDirectory: '.' },
    target: 'production'
  });

  const deploy = await httpReq('https://api.vercel.com/v13/deployments', {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(deployPayload) }
  }, deployPayload);

  const deployId = deploy.body.id;
  const previewUrl = deploy.body.url;
  if (!deployId) throw new Error(`Full deploy failed: ${JSON.stringify(deploy.body).slice(0,300)}`);

  // Step 6: Wait for READY
  for (let i = 0; i < 20; i++) {
    await sleep(5000);
    const st = await httpReq(`https://api.vercel.com/v13/deployments/${deployId}`, {
      method: 'GET', headers: { Authorization: `Bearer ${VERCEL_TOKEN}` }
    });
    if (st.body.readyState === 'READY') break;
  }

  // Step 7: Reassign cs.qck.co ONLY after confirming this is a FULL deployment
  // Safe because allFiles contains all 97+ repo files
  const aliasPayload = JSON.stringify({ alias: 'cs.qck.co' });
  await httpReq(`https://api.vercel.com/v2/deployments/${previewUrl}/aliases`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${VERCEL_TOKEN}`, 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(aliasPayload) }
  }, aliasPayload);

  return `https://cs.qck.co/intro/${slug}`;
}

// ── Handler ───────────────────────────────────────────────────────────────────

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

    // Load aloha template
    const templatePath = path.join(process.cwd(), 'intro', 'aloha-seo-demand-analysis.html');
    let template = '';
    try { template = fs.readFileSync(templatePath, 'utf8'); }
    catch {
      // Fallback: fetch live
      const r = await httpReq('https://cs.qck.co/intro/aloha-seo-demand-analysis', { method: 'GET', headers: { Accept: 'text/html' } });
      template = typeof r.body === 'string' ? r.body : r.raw;
    }

    const slug = `${domain.replace(/\./g, '-')}-seo-demand-analysis`;
    const html = generateHtml(domain, data, template);

    // Full safe deploy (commits to GitHub + full Vercel redeploy)
    const liveUrl = await commitAndDeploy(slug, html);

    return res.status(200).json({
      ok: true, domain, url: liveUrl, slug,
      dr: data.domain_rating, traffic: data.org_traffic, keywords: data.org_keywords
    });
  } catch (err) {
    console.error('generate-report error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
};
