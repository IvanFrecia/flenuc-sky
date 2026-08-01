# Audit: SkyLabs Developments org brand vs personal portfolio

**Project:** `/home/skye/Projects/flenuc-sky`  
**Owner intent:** Personal portfolio only (Ivan Frecia) — not SkyLabs Developments as organization/corporate brand.  
**Audit date:** 2026-08-01  
**Scope:** Full monorepo text sources (`.md`, `.html`, `.py`, `.json`, `.sh`, etc.). Excluded: `.git`, `.venv`, `__pycache__`, `node_modules`.  
**Action taken:** Audit only — **no files modified**.

---

## 1. Executive summary

The site and content kit are **heavily framed as a company brand** (“SkyLabs Developments” / “SkyLabs”), not a personal portfolio. Marketing UI, SEO titles, legal operator blocks, campaign titles, Stripe product names, social strategy, and README all present an **org identity**.

| Metric | Count |
|--------|------:|
| Files with brand hits | **35** |
| Total match lines (SkyLabs / skylabs / Developments) | **~145** |
| **P0** marketing / legal / UI org brand | **~95** lines (incl. legal dual-copy) |
| **P1** ambiguous (handle/domain/email strategy) | **~35** lines |
| **P2** infra-only (GCP project ids, billing notes) | **~10** lines |
| `freciaivan@gmail.com` present | **0** (not used) |
| Contact email in code | `ifrecia@skylabs-developments.tech` only |
| NDA brands **used** as marketing (Heroes, Raise X) | **0** (only “never use” warnings) |
| Allowed personal assets present | Ivan Frecia name, GitHub `IvanFrecia`, product Sky Colab |

**Verdict:** Personal rebrand is **required** across live UI, config defaults, legal packages (×2 copies), campaign copy, and social launch kit before treating this as a personal portfolio.

---

## 2. Severity legend

| Severity | Meaning |
|----------|---------|
| **P0** | Live marketing / legal / product UI framing as **SkyLabs Developments** (or “SkyLabs” company). Must rebrand for personal portfolio. |
| **P1** | Ambiguous: org domain/email/handle used as contact or social identity; could stay as personal infra if reframed, but currently org-coded. |
| **P2** | Infra-only: GCP project IDs, billing account labels, deploy notes — not marketing brand. Note only. |

---

## 3. Findings table

### 3.1 Site config & app shell (P0 / P1)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `apps/portfolio/app/config.py` | 50 | `contact_email: str = "ifrecia@skylabs-developments.tech"` | P1 |
| `apps/portfolio/app/config.py` | 51 | `site_name: str = "Ivan Frecia · SkyLabs"` | **P0** |
| `apps/portfolio/app/main.py` | 17 | `title="Flenuc Sky — Ivan Frecia / SkyLabs"` | **P0** |
| `apps/portfolio/app/__init__.py` | 1 | `"""Flenuc Sky — Ivan Frecia / SkyLabs portfolio + rewards fund."""` | P1 |
| `apps/portfolio/app/templates/base.html` | 14 | `og:site_name` → `{{ site_name }}` (inherits P0 default) | **P0** |
| `apps/portfolio/app/templates/partials/nav.html` | 7 | `<span class="brand-sub">SkyLabs</span>` | **P0** |
| `apps/portfolio/app/templates/partials/footer.html` | 4 | `Ivan Frecia · SkyLabs Developments` | **P0** |
| `apps/portfolio/app/templates/partials/footer.html` | 41 | `© … Ivan Frecia / SkyLabs Developments.` | **P0** |
| `apps/portfolio/app/templates/legal/page.html` | 11 | `© … Ivan Frecia / SkyLabs Developments ·` | **P0** |
| `apps/portfolio/app/templates/home.html` | 6 | `Ivan Frecia · SkyLabs` | **P0** |
| `apps/portfolio/app/templates/home.html` | 10 | `under <strong>SkyLabs Developments</strong>` | **P0** |
| `apps/portfolio/app/templates/about.html` | 8 | `Founder and engineer at <strong>SkyLabs Developments</strong>` | **P0** |
| `apps/portfolio/app/templates/about.html` | 20–22 | `<h2>SkyLabs</h2>` + “SkyLabs is the product and R&D home…” | **P0** |
| `apps/portfolio/app/templates/sky_colab.html` | 8 | `tooling from SkyLabs` | **P0** |
| `apps/portfolio/app/templates/sky_colab.html` | 22 | `open reference surface for SkyLabs multi-model systems` | **P0** |
| `apps/portfolio/app/templates/contact.html` | 25 | `Blog · skylabs-developments.tech` | P1 |

### 3.2 Page titles & meta (P0)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `apps/portfolio/app/routers/pages.py` | 31 | default description: `Ivan Frecia · SkyLabs — …` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 55–56 | home title/desc with SkyLabs | **P0** |
| `apps/portfolio/app/routers/pages.py` | 66 | `About · Ivan Frecia / SkyLabs` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 130 | `Work · Ivan Frecia / SkyLabs` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 141–142 | `sky-colab · SkyLabs` / `tooling by SkyLabs` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 154–155 | `Rewards Campaign · SkyLabs` / `Support SkyLabs R&D` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 170 | `KPI Dashboard · SkyLabs` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 182 | `Contact · Ivan Frecia / SkyLabs` | **P0** |
| `apps/portfolio/app/routers/pages.py` | 192, 208, 217 | `Legal · SkyLabs` / `f"{title} · SkyLabs"` | **P0** |

### 3.3 Campaign, Stripe, ledger (P0)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `apps/portfolio/app/services/fund.py` | 58 | `"id": "skylabs-rewards-5d-202608"` | P1 (id) / **P0** if user-visible |
| `apps/portfolio/app/services/fund.py` | 59 | `"title": "5-Day SkyLabs Rewards Sprint"` | **P0** |
| `apps/portfolio/app/services/stripe_service.py` | 45 | `f"SkyLabs Rewards — {tier['name']}"` | **P0** (checkout line item) |
| `apps/portfolio/data/ledger.json` | 3 | `"campaign_id": "skylabs-rewards-5d-202608"` | P1 |

### 3.4 Social data & services (P0 / P1)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `apps/portfolio/app/data/social.json` | 5 | `blog: https://skylabs-developments.tech/` | P1 |
| `apps/portfolio/app/data/social.json` | 6–7 | `x.com/SkyLabsDev`, `@SkyLabsDev` | P1 |
| `apps/portfolio/app/data/social.json` | 9 | `email: ifrecia@skylabs-developments.tech` | P1 |
| `apps/portfolio/app/data/social.json` | 11 | fallbacks `@SkyLabsDevs` → `@SkyLabsHQ` | P1 |
| `apps/portfolio/app/data/social.json` | 12 | `company page SkyLabs Developments secondary` | **P0** (strategy as company) |
| `apps/portfolio/app/services/social.py` | 16–20 | defaults: blog/X/email skylabs… | P1 |

### 3.5 Legal — live package + app fallback (duplicate copies) (P0)

Primary source in Docker: `packages/legal/`. Fallback: `apps/portfolio/app/legal_md/`. Content is mirrored — **both must be rebranded** or one deleted after single-source fix.

| File (each pair) | Line(s) | Snippet | Severity |
|------------------|--------:|---------|----------|
| `packages/legal/*.md` + `apps/portfolio/app/legal_md/*.md` | 4 | `**Operator:** Ivan Frecia / SkyLabs Developments` | **P0** |
| same (all 5 docs) | 5 | `**Contact:** ifrecia@skylabs-developments.tech` | P1 |
| `…/terms.md` | 24 | `affiliation with Ivan Frecia or SkyLabs Developments` | **P0** |
| `…/terms.md` | 28 | `© Ivan Frecia / SkyLabs Developments` | **P0** |
| `…/privacy.md` | 52–53 | Operator block: SkyLabs Developments + email | **P0** / P1 |
| `…/rewards.md` | 14 | `no ownership of SkyLabs Developments` | **P0** |
| `…/refunds.md` | 41 | `© 2026 Ivan Frecia / SkyLabs Developments` | **P0** |
| Contact lines in all legal | various | `ifrecia@skylabs-developments.tech` | P1 |

**Docs:** privacy, terms, rewards, risk, refunds × **2 trees** ≈ **~40 P0/P1 lines** in legal alone.

### 3.6 Content / social launch kit (P0)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `content/social/HANDLES_AND_CALENDAR.md` | 1 | title: `SkyLabs / Sky Colab` | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 3 | `**Brand:** SkyLabs Developments` | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 8–10 | blog/email skylabs-developments | P1 |
| `content/social/HANDLES_AND_CALENDAR.md` | 20–34 | `@SkyLabsDev`, display `Ivan Frecia · SkyLabs` | P1 / **P0** display |
| `content/social/HANDLES_AND_CALENDAR.md` | 57 | `Company page (SkyLabs Developments)` | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 64–72 | Founder of company + LinkedIn company name | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 95–113 | bios: “founder of SkyLabs Developments”, “OSS by SkyLabs” | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 128 | `SkyLabs is building in public` | **P0** |
| `content/social/HANDLES_AND_CALENDAR.md` | 154–170 | brand links + mailto skylabs | P1 |
| `content/social/LAUNCH_KIT.md` | 1 | `Social launch kit — SkyLabs / …` | **P0** |
| `content/social/LAUNCH_KIT.md` | 15, 26 | site URL `https://skylabs-developments.com` | P1 |
| `content/social/LAUNCH_KIT.md` | 34 | `SkyLabs weekly transparency` | **P0** |
| `content/social/LAUNCH_KIT.md` | 39 | `skylabs-developments.com/kpi` | P1 |

### 3.7 README & product docs (P0 / P1)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `README.md` | 3 | `**Ivan Frecia · SkyLabs Developments**` | **P0** |
| `README.md` | 31 | Hero — `Ivan Frecia · SkyLabs` | **P0** |
| `README.md` | 103–104 | email + `© … SkyLabs Developments` | **P0** / P1 |
| `docs/overview.md` | 5 | `Personal + SkyLabs portfolio site` | **P0** |
| `docs/overview.md` | 24 | Contact email skylabs domain | P1 |
| `docs/DOMAIN_HOSTINGER.md` | 1+ | Domain ops for `skylabs-developments.com` | P1 (domain strategy) / P2 (DNS steps) |
| `docs/DOMAIN_HOSTINGER.md` | 12 | gcloud account `ifrecia@skylabs-developments.tech` | P2 / P1 |

### 3.8 Infra-only (P2) — keep; not marketing brand

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `docs/BILLING_QUOTA.md` | 4 | org `skylabs-developments.tech` (GCP org) | **P2** infra id |
| `docs/BILLING_QUOTA.md` | 5, 7, 29 | billing `skylabs`, project `skylabs-devops` | **P2** |
| `docs/LIVE.md` | 8 | Project `skylabs-devops` | **P2** |
| `apps/portfolio/app/services/kpi.py` | 131 | `host: "skylabs-devops (interim; …)"` | **P2** (visible on KPI page — consider soft-label if public) |
| `infra/scripts/bootstrap-infra.sh` | 5 | default GCP `ACCOUNT=…@skylabs-developments.tech` | **P2** |

> **Note:** KPI `host` string is user-visible on `/kpi`. Technically an infra label; if the dashboard is public marketing, soft-rename to “Cloud Run (production)” to avoid company bleed.

### 3.9 NDA third-party brands (Heroes, Raise X)

| File | Line | Snippet | Severity |
|------|-----:|---------|----------|
| `content/social/HANDLES_AND_CALENDAR.md` | 5 | `**Never** use names related to Heroes, Raise X…` | OK (policy only) |
| `content/social/HANDLES_AND_CALENDAR.md` | 84 | `Avoid Heroes / Raise X / NDA client names` | OK (policy only) |
| `content/social/LAUNCH_KIT.md` | 3 | `Do not mention third-party NDA product names` | OK |

**No live product UI or legal text names Heroes / Raise X.** Keep the “never use” rules; do not promote those brands.

### 3.10 Allowed / keep (personal & product)

| Asset | Status |
|-------|--------|
| Name **Ivan Frecia** | OK — primary brand going forward |
| GitHub **IvanFrecia** / **sky-colab** | OK |
| Product name **Sky Colab** / **sky-colab** | OK if framed as *personal* OSS, not “by SkyLabs Developments” |
| LinkedIn `linkedin.com/in/ivanfrecia` | OK personal |
| GCP project `flenuc-sky`, service names | P2 infra — OK |

---

## 4. Recommended personal rebrand

### 4.1 Positioning

| Surface | Current (org) | Target (personal) |
|---------|---------------|-------------------|
| Site identity | Ivan Frecia · SkyLabs / SkyLabs Developments | **Ivan Frecia** — personal portfolio |
| Nav sub-brand | SkyLabs | drop, or “Portfolio” / “Engineer” / omit |
| Product section | sky-colab by SkyLabs | **Sky Colab** — personal OSS project |
| Campaign | 5-Day SkyLabs Rewards Sprint | **Ivan Frecia · 5-Day Rewards Sprint** |
| Stripe line items | SkyLabs Rewards — {tier} | Ivan Frecia Rewards — {tier} (or “Portfolio Rewards”) |
| Legal operator | Ivan Frecia / SkyLabs Developments | **Ivan Frecia** (sole operator) |
| Copyright | © Ivan Frecia / SkyLabs Developments | **© {year} Ivan Frecia** |
| Social strategy | Company page secondary | Personal-only; no company page required |

### 4.2 Contact email (choose one)

| Option | Value | Notes |
|--------|-------|--------|
| **A (preferred personal)** | `freciaivan@gmail.com` | Clear personal contact; no org domain. **Not present in repo today.** |
| **B (keep domain email)** | `ifrecia@skylabs-developments.tech` | Acceptable **only if** framed as *personal* contact and legal operator is “Ivan Frecia” alone — not “SkyLabs Developments”. Prefer updating public copy to avoid org implication. |
| **C (hybrid)** | Public: Gmail; infra/GCP: skylabs domain | Best of both: marketing clean, infra unchanged (P2). |

**Audit note:** Every legal doc and `config.contact_email` currently use the skylabs domain. If switching to Gmail, update config + social.json + legal contact blocks + README together.

### 4.3 Domains & handles (decision outside pure string replace)

| Item | Recommendation |
|------|----------------|
| `skylabs-developments.com` as public portfolio URL | Prefer personal domain or keep Cloud Run URL; if domain stays, site copy must still read as **personal**, not company. |
| `skylabs-developments.tech` blog | Keep as personal blog URL or rebrand later; label as “Blog”, not company site. |
| `@SkyLabsDev` | P1 — company-coded handle. Prefer `@IvanFrecia` or product `@skycolab` for personal portfolio narrative. |
| LinkedIn company page plan | **Drop** from strategy docs for personal-only launch. |

### 4.4 Campaign IDs

- Human title: `Ivan Frecia · 5-Day Rewards Sprint`
- Machine id (`skylabs-rewards-5d-202608`): can remain for ledger continuity (P1) or migrate to `ivan-frecia-rewards-5d-202608` if no live payments depend on it.

### 4.5 Legal dual-copy hygiene

`config.py` resolves legal from `packages/legal` first, then `app/legal_md`. After rebrand:

1. Edit **canonical** tree (`packages/legal/`).
2. Sync or delete `apps/portfolio/app/legal_md/` to avoid stale operator text in fallback path.
3. Confirm Docker image copies `packages/legal` (it does).

---

## 5. Suggested fix order (for a later implementation pass — not done here)

1. **P0 UI shell:** `config.site_name`, nav, footer, home, about, sky_colab, legal/page copyright.  
2. **P0 titles:** all `page_title` / `page_description` in `pages.py` + `main.py` FastAPI title.  
3. **P0 campaign:** `fund.py` title (+ optional id), `stripe_service.py` product name.  
4. **P0 legal:** operator/copyright in `packages/legal/*` and mirror `legal_md/*`.  
5. **P0 social kit:** `HANDLES_AND_CALENDAR.md`, `LAUNCH_KIT.md`, `social.json` company-page notes.  
6. **P1 contact:** email + blog labels + X handle strategy.  
7. **README / docs/overview** marketing lines.  
8. **Leave P2** GCP project ids / billing docs as infra notes (annotate “infra id, not marketing brand” if desired).  
9. Soft-edit KPI host string if public.

---

## 6. Top 15 P0 items (priority fix list)

1. **`apps/portfolio/app/templates/partials/footer.html:4`** — footer brand `Ivan Frecia · SkyLabs Developments`  
2. **`apps/portfolio/app/templates/partials/footer.html:41`** — copyright `SkyLabs Developments`  
3. **`apps/portfolio/app/templates/partials/nav.html:7`** — brand-sub `SkyLabs`  
4. **`apps/portfolio/app/config.py:51`** — `site_name = "Ivan Frecia · SkyLabs"` (feeds OG `site_name`)  
5. **`apps/portfolio/app/templates/home.html:10`** — hero claims work under **SkyLabs Developments**  
6. **`apps/portfolio/app/templates/about.html:8,20–22`** — founder at company + “SkyLabs” R&D section  
7. **`apps/portfolio/app/services/fund.py:59`** — campaign title `5-Day SkyLabs Rewards Sprint`  
8. **`apps/portfolio/app/services/stripe_service.py:45`** — Stripe product `SkyLabs Rewards — …`  
9. **`apps/portfolio/app/routers/pages.py`** — all `page_title` / descriptions with SkyLabs (home, about, work, sky-colab, fund, kpi, contact, legal)  
10. **`packages/legal/*.md` (+ `legal_md` mirror)** — Operator `Ivan Frecia / SkyLabs Developments` on all five legal docs  
11. **`packages/legal/terms.md:28`** (and mirror) — site content © SkyLabs Developments  
12. **`packages/legal/rewards.md:14`** (and mirror) — ownership of SkyLabs Developments  
13. **`apps/portfolio/app/templates/sky_colab.html:8,22`** — product framed as from/for SkyLabs  
14. **`content/social/HANDLES_AND_CALENDAR.md`** — Brand/company page/bios framed as SkyLabs Developments org  
15. **`content/social/LAUNCH_KIT.md` + `README.md:3,104`** — launch/marketing copy as SkyLabs company  

---

## 7. File inventory (35 files with hits)

```
README.md
apps/portfolio/app/__init__.py
apps/portfolio/app/config.py
apps/portfolio/app/main.py
apps/portfolio/app/data/social.json
apps/portfolio/app/routers/pages.py
apps/portfolio/app/services/fund.py
apps/portfolio/app/services/kpi.py
apps/portfolio/app/services/social.py
apps/portfolio/app/services/stripe_service.py
apps/portfolio/app/templates/about.html
apps/portfolio/app/templates/contact.html
apps/portfolio/app/templates/home.html
apps/portfolio/app/templates/legal/page.html
apps/portfolio/app/templates/partials/footer.html
apps/portfolio/app/templates/partials/nav.html
apps/portfolio/app/templates/sky_colab.html
apps/portfolio/app/legal_md/{privacy,terms,rewards,risk,refunds}.md
apps/portfolio/data/ledger.json
content/social/HANDLES_AND_CALENDAR.md
content/social/LAUNCH_KIT.md
docs/BILLING_QUOTA.md
docs/DOMAIN_HOSTINGER.md
docs/LIVE.md
docs/overview.md
infra/scripts/bootstrap-infra.sh
packages/legal/{privacy,terms,rewards,risk,refunds}.md
```

(`base.html` inherits P0 via `site_name`; no literal “SkyLabs” string.)

---

## 8. Out of scope / not found

- No `freciaivan@gmail.com` in repo (must be introduced if preferred contact).  
- No env example files with SkyLabs strings.  
- Dockerfile has no brand strings.  
- No live Heroes / Raise X product naming (only avoidance notes).  

---

## 9. Sign-off

This audit is **read-only**. Rebrand implementation should be a separate change set with visual QA (home, about, footer, fund, legal pages, Stripe checkout demo) and dual legal tree sync.

**Report path:** `/home/skye/Projects/flenuc-sky/docs/AUDIT_PERSONAL_BRAND.md`
