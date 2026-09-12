# aicrazed.com

An independent directory of official customer service contact info — phone numbers, chat links, and support hours — verified directly against each company's own website. Not affiliated with any company listed.

Live at [aicrazed.com](https://aicrazed.com), hosted on Netlify, source on GitHub at `kdtichi/aicrazed`.

## How it's built

Static site, no framework, no build-time dependencies beyond the Python 3 standard library. `build/build.py` reads `data/brands.json` and renders every page as plain HTML into `dist/`. Netlify runs that same command on every push (see `netlify.toml`) and serves `dist/` directly — nothing server-side, no database.

```
data/brands.json      Single source of truth: site copy, categories, and all 28 brands
build/build.py         The generator — reads brands.json, writes dist/
build/serve.py          Local static file server (works around a sandbox getcwd bug — see file header)
public/                Static assets copied into dist/ as-is: CSS, JS, favicon, logo, OG images
dist/                  Generated output (gitignored) — this is what actually gets deployed
netlify.toml           Netlify build command + publish directory
```

### Rebuild after editing data

```bash
python3 build/build.py
```

### Preview locally

```bash
cd dist && python3 -m http.server 4173
```

Then open `http://127.0.0.1:4173`. (`build/serve.py` also works and avoids a sandbox quirk with plain `http.server` in some environments — see the comment at the top of that file.)

### Deploy

Netlify auto-builds and redeploys on every push to `main`:

```bash
git add -A && git commit -m "..." && git push
```

## Adding or editing a brand

Everything lives in `data/brands.json`. Add an object to the `brands` array:

```json
{
  "slug": "example",
  "name": "Example Inc",
  "category": "retail",
  "aliases": ["example customer service", "example support number"],
  "phone": "1-800-555-0100",
  "phoneNote": "",
  "phoneAltNote": "",
  "chatUrl": "https://example.com/help",
  "chatLabel": "Example Help Center",
  "hours": { "mode": "247" },
  "verifiedDate": "2026-09-12",
  "sourceUrl": "https://example.com/contact",
  "sourceLabel": "Example Contact Us page",
  "commonIssues": ["Order not delivered", "Refund status", "Account access"],
  "avgWaitTime": "",
  "bestTimeToCall": "",
  "scamWarningNote": ""
}
```

**Rules that matter, learned the hard way this project:**

- **Never invent a phone number, hours, or a fact you can't source.** If a company doesn't publish a phone number, set `"phone": null` and explain why in `phoneAltNote` — the page will render an honest "does not publish a number" notice instead. This site's entire value proposition is that every fact is checked against the company's own official page; a wrong number here is worse than no number.
- **`sourceUrl` must be the company's own official domain**, never a forum, review site, or aggregator. `verifiedDate` is the date you actually checked it — don't bump it to "today" just to look fresh; that's what `sitemap.xml`'s `lastmod` and the on-page "Verified" stamp both key off of.
- **`hours.mode`** is one of three shapes:
  - `{"mode": "247"}` — literally 24/7, no other fields needed.
  - `{"mode": "unspecified", "text": "..."}` — full sentence for when hours aren't published, or vary in a way the `detailed` mode can't represent (e.g. different weekday/weekend hours) — see AT&T or Coinbase-era entries for tone.
  - `{"mode": "detailed", "tz": "America/Los_Angeles", "start": "04:00", "end": "21:00", "days": "daily"}` — a single daily window in the company's own timezone. `public/js/hours.js` converts this to the visitor's local time client-side and shows an "Open now"/"Closed now" badge. Only use this when the company publishes one clean daily window — don't force weekday/weekend splits into it.
- **`avgWaitTime` / `bestTimeToCall`** should almost always stay `""` (empty) so the page falls back to honest, non-brand-specific guidance ("Not officially published" / "Early or late in the day"). Only fill these in if you have an actual sourced figure — this was originally shipped with a fabricated-sounding number for Temu and had to be walked back; see git history around the first commit if you want the cautionary tale.
- **Categories** live in the same file's `categories` object, each with a `description` (short, used in meta/lede) and an `intro` (100–200 words of real, category-specific copy — not boilerplate, see the existing five for the pattern). Adding a category also needs an SVG icon added to `CATEGORY_ICONS` in `build.py`.
- **`featuredBrands`** (under `site` in the JSON) controls the home page's curated grid of 12 — it's a subset, not the full list. Search (`public/js/search.js`) always covers every brand regardless of what's featured.

After editing, always run `python3 build/build.py` and spot-check the affected page before pushing — there's no CI, so a typo in a `.format()` placeholder fails loud and immediate (good) but only if you actually run the build.

## Generating a new brand's OG image

Per-brand social share images (`public/og/{slug}.png`, 1200×630) are rendered via a headless Canvas 2D script, not committed as source — see the session history for the exact HTML/JS harness (`renderBrandImage(name)` in a scratch `og-canvas-brand.html`) if you need to regenerate one. The short version: open that harness in a real browser tab pointed at the local dev server, call `renderBrandImage("Brand Name")`, pull the canvas's `toDataURL()` output, and decode it to a PNG. Tedious enough that it's worth batching multiple brands per page load if you're doing more than one.

## Design system

Type-led, restrained palette, hairline rules — deliberately not another rounded-corner SaaS template. Fraunces (serif, headings) + Inter (sans, body), loaded from Google Fonts with a **working opt-out**: the footer's "Turn off Google Fonts" toggle sets `localStorage['aicrazed-fonts-optout']`, which prevents the font `<link>` tags from ever being created (see the inline script in `layout()` in `build.py`) — not just a CSS swap, the network request itself never fires. Falls back cleanly to Georgia/system-ui.

All icons and illustrations are original inline SVG line art (see `CATEGORY_ICONS`, `ABOUT_ICON`, `HOW_IT_WORKS_ICON` in `build.py`) — no stock photography, no real company logos, by deliberate design choice given how trademark-sensitive this niche is.

## Content policy this project actually follows

- Independence disclaimer on every single page (the black ribbon under the header) — never optional, never buried.
- No brand's logo or visual identity used anywhere — every listing is identified by name only, in aicrazed's own visual system.
- No fabricated stats, no fake "X users helped" counters, no stock photos of headset-wearing agents.
- Every claim about a company (phone number, hours, chat link) traces to a `sourceUrl` on that company's own domain, with a visible verification date.
- When research couldn't confirm something (a blocked domain, a conflicting number, a suspected scam number circulating online), the brand was either left out entirely or the uncertainty was stated on the page — never silently resolved by guessing. See `docs/advertising-compliance.md` for the paid-advertising implications of this category, and `/editorial-policy/` on the live site for the public-facing version of these standards.

## Known constraints

- No Node/npm/Homebrew on the original dev machine — the entire build is Python stdlib only, on purpose. Don't add an npm dependency without a good reason.
- `preview_start`-style dev-server tooling had a sandbox bug (denied `getcwd()`) in the original environment; `build/serve.py` works around it by never calling `os.getcwd()`. If dev-server tooling fails mysteriously in a similar way, that's likely why.
