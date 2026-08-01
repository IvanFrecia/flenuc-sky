# Social handles, bios & 5-day calendar — Ivan Frecia / Sky Colab

**Brand:** Ivan Frecia (personal) · **Product:** Sky Colab (Apache-2.0)  
**Rules:** Rewards campaign is **not equity**. Never claim guaranteed profit, assured ROI, or investment returns.  
**Never** use names related to Heroes, Raise X, or NDA clients.

**Live site (primary):** https://sky-portfolio-6k4smyyquq-uc.a.run.app  
**Repo:** https://github.com/IvanFrecia/sky-colab  
**Contact:** freciaivan@gmail.com

Machine-readable links: `apps/portfolio/app/data/social.json`

---

## 1. X / Twitter — personal handle

| Rank | Handle | Rationale | Availability note |
|------|--------|-----------|-------------------|
| **1 (recommended)** | **`@IvanFrecia`** | Matches GitHub `IvanFrecia`; strongest founder trust; personal brand only. | **Claim if available.** |
| 2 | `@skycolab` | Product-first secondary; memorable for repo/docs/demo posts. | Optional product account only — not a company brand. |

### Recommended primary

**Use `@IvanFrecia` as the single primary account** (personal voice only).

**Display name:** `Ivan Frecia`  
**Location / link in bio:** Portfolio run.app URL (swap to a personal custom domain when DNS is live).  
**GitHub profile:** set `twitter_username` to the claimed handle once reserved.

### X profile wiring (checklist)

- [ ] Claim handle + set display name + avatar (use portfolio `avatar.png`)
- [ ] Header: simple dark board / collab diagram or product screenshot
- [ ] Pin Day-1 launch post (see calendar)
- [ ] Website field → portfolio interim URL
- [ ] Enable creator/professional label if offered; category: Software / AI
- [ ] Update GitHub: Settings → Public profile → Twitter username
- [ ] Cross-link from portfolio footer + LinkedIn Contact info

---

## 2. LinkedIn — personal only

### Strategy

| Asset | Role | Priority |
|-------|------|----------|
| **Personal profile (Ivan Frecia)** | Primary and only channel. Trust, DMs, reposts, partner discovery. | **Ship first** |

**No company page.** This is a personal portfolio; do not create or promote a company page for this project.

### Personal profile setup

- **Headline (≤220 chars):**  
  `Building Sky Colab — open multi-model collaboration (Apache-2.0) · Applied product engineering · Personal portfolio`
- **Featured:** repo, portfolio, fund/rewards page
- **Experience:** Independent engineer / open-source maintainer (current); link personal portfolio
- **Contact info:** email `freciaivan@gmail.com`, website (run.app), X handle, GitHub
- **Custom URL:** claim `linkedin.com/in/ivanfrecia` if available; else `ivan-frecia`

### Posting rules

1. Publish on **personal** profile only.  
2. No equity/ROI language.  
3. Always link legal/rewards pages when mentioning the campaign.  
4. Avoid Heroes / Raise X / NDA client names entirely.

---

## 3. Bio copy

### X / Twitter (≤160 characters)

**Recommended:**

```
Ivan Frecia. Building Sky Colab — open multi-model collab with a transparent board (Apache-2.0). Rewards campaign open (not equity).
```

**Alt A (product-forward):**

```
Sky Colab: multi-model collab · structured handoffs · challenge mode · audit trail. OSS by Ivan Frecia. Rewards campaign (not investment).
```

**Alt B (founder + links):**

```
Ivan Frecia. Open-source multi-model systems. Sky Colab on GitHub. Portfolio + rewards sprint below ↓
```

### LinkedIn About (3 sentences)

```
I'm Ivan Frecia — applied product engineering for multi-model systems. Sky Colab is my Apache-2.0 open-source project: agents exchange reviewed work on a shared board with structured handoffs, challenge mode, and an audit trail (not free-form multi-chat). I'm also running a short rewards-style campaign to cover product ops and continued build work — not equity, no profit guarantees; details and terms live on the site.
```

---

## 4. Five-day content calendar

**Goal of sprint:** awareness for Sky Colab + transparent rewards campaign (~$20 ops+floor context is *internal*; public posts talk mission, product, and rewards tiers — never profit guarantees).  
**Cadence:** 1 primary post/day on X + LinkedIn (same core message, platform-native length).  
**Tone:** build-in-public, technical, honest. No “guaranteed returns,” “passive income,” or investment framing.

| Day | Theme | X post (copy-ready) | LinkedIn angle | CTA |
|-----|--------|---------------------|----------------|-----|
| **1** | Launch / what it is | Shipping **Sky Colab** open source: multi-model collab with a transparent board — structured handoffs, challenge mode, audit trail. Apache-2.0 · CLI duo. Repo: https://github.com/IvanFrecia/sky-colab · Site: https://sky-portfolio-6k4smyyquq-uc.a.run.app | Longer: problem (chat spaghetti) → board model → link repo + portfolio. Mention rewards campaign only as “supporting continued product work (not equity).” | Star repo / visit site |
| **2** | How it works | Sky Colab isn’t multi-chat free-for-all. Flow: prompts → responses → handoffs → challenge → audit. Designed so humans can *see* the work product trail. #OpenSource #SkyColab | Diagram or numbered steps (5 bullets). Invite engineers to clone and try CLI duo. | Repo README |
| **3** | Why open source | Why Apache-2.0: fork it, audit it, extend it. Multi-model systems need transparent process as much as clever prompts. Building in public. | Story: what “transparent board” means for teams that care about reviewability. | GitHub |
| **4** | Rewards sprint (compliance-safe) | Opening a **rewards / pre-order style** campaign to fund continued Sky Colab work — **not equity, not securities, no profit guarantees**. Tiers + legal terms on the site. Portfolio: https://sky-portfolio-6k4smyyquq-uc.a.run.app/fund | Full clarity: what backers get (digital rewards / support), what they don’t (ownership, ROI). Link `/legal/rewards` + `/legal/risk`. | Fund page |
| **5** | Transparency + invite | Closing the 5-day sprint: product shipped open, rewards page live, KPI page for public metrics. Thanks to early stars & readers. Next: keep shipping. Star / back / feedback welcome. KPI: …/kpi | Recap thread: shipped · learned · next milestones. Invite comments + email for partnerships: freciaivan@gmail.com | KPI + contact |

### Optional hashtags (use sparingly)

`#OpenSource` `#AI` `#MultiAgent` `#SkyColab` `#BuildInPublic`

### Compliance checklist (every campaign mention)

- [ ] “Not equity / not securities”  
- [ ] “No guaranteed profit or assured ROI”  
- [ ] Link to rewards terms / risk when asking for support  
- [ ] No third-party NDA product names  

---

## 5. Footer / social link set (hardcode on portfolio)

Use these exact destinations in `partials/footer.html` (and any share meta). Source of truth: `apps/portfolio/app/data/social.json`.

| Label | URL |
|-------|-----|
| GitHub | https://github.com/IvanFrecia |
| Sky Colab | https://github.com/IvanFrecia/sky-colab |
| Website | https://sky-portfolio-6k4smyyquq-uc.a.run.app |
| X | https://x.com/IvanFrecia |
| LinkedIn | https://www.linkedin.com/in/ivanfrecia |
| Email | mailto:freciaivan@gmail.com |

**Suggested footer row (copy order):** GitHub · Sky Colab · X · LinkedIn · Contact

**Suggested HTML fragment (optional paste):**

```html
<nav class="footer-social" aria-label="Social">
  <a href="https://github.com/IvanFrecia" rel="me noopener" target="_blank">GitHub</a>
  <a href="https://github.com/IvanFrecia/sky-colab" rel="noopener" target="_blank">Sky Colab</a>
  <a href="https://x.com/IvanFrecia" rel="me noopener" target="_blank">X</a>
  <a href="https://www.linkedin.com/in/ivanfrecia" rel="me noopener" target="_blank">LinkedIn</a>
  <a href="mailto:freciaivan@gmail.com">Email</a>
</nav>
```

After handles are claimed, if you used a fallback X handle, update both this doc and `social.json` in the same PR.

---

## Wiring order (execute in ~30 minutes)

1. Claim X `@IvanFrecia` (or first free personal fallback) → paste X bio → pin Day-1 post.  
2. Claim LinkedIn vanity URL → paste About + headline → Featured links.  
3. Set GitHub `twitter_username` + website.  
4. Point portfolio footer at `social.json` fields.  
5. Run Days 1–5 calendar; log metrics on `/kpi`.

---

## Internal only (do not post)

- Sprint math: cover ~$10 ops + ~$10 profit floor ≈ **$20 goal** for this micro-sprint.  
- Public framing stays product + rewards tiers + transparency — never “guaranteed profit.”
