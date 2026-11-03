"""
"No phone support" report: a citable, data-driven page generated entirely
from data/brands.json.

Every number on this page is computed from listings that were each checked
against the company's own site — nothing here is estimated or written by
hand. It exists because a single page that answers "which big companies
don't publish a customer service number?" with a dated, sourced table is the
kind of thing AI answer engines and journalists quote.
"""
import csv
import io
import json

REPORT_PATH = "/reports/no-phone-support/"
REPORT_CSV_PATH = "/reports/no-phone-support.csv"
REPORT_TITLE = "Which Major US Companies Don't Publish a Customer Service Phone Number?"

CHANNEL_LABELS = {"chat": "Live chat", "form": "Contact form", "none": "Help center"}


def channel_label(brand: dict) -> str:
    return CHANNEL_LABELS[brand.get("chatType", "form")]


def report_rows(brands: list, categories: dict) -> list:
    """One row per brand, no-phone companies first, then by category order and name."""
    cat_order = {slug: i for i, slug in enumerate(categories)}
    rows = [
        {
            "name": b["name"],
            "slug": b["slug"],
            "category": categories[b["category"]]["label"],
            "category_slug": b["category"],
            "phone_published": bool(b.get("phone")),
            "channel": channel_label(b),
            "verified": b["verifiedDate"],
            "source": b["sourceUrl"],
        }
        for b in brands
    ]
    return sorted(rows, key=lambda r: (r["phone_published"], cat_order[r["category_slug"]], r["name"].lower()))


def report_stats(rows: list, categories: dict) -> dict:
    total = len(rows)
    no_phone = [r for r in rows if not r["phone_published"]]
    by_cat = []
    for slug, cat in categories.items():
        members = [r for r in rows if r["category_slug"] == slug]
        if not members:
            continue
        missing = sum(1 for r in members if not r["phone_published"])
        by_cat.append({"slug": slug, "label": cat["label"], "total": len(members), "no_phone": missing})
    no_phone_channels = {}
    for r in no_phone:
        no_phone_channels[r["channel"]] = no_phone_channels.get(r["channel"], 0) + 1
    return {
        "total": total,
        "no_phone": len(no_phone),
        "pct": round(100 * len(no_phone) / total) if total else 0,
        "by_cat": by_cat,
        "no_phone_channels": no_phone_channels,
        "oldest": min(r["verified"] for r in rows),
        "newest": max(r["verified"] for r in rows),
    }


def render_report_csv(rows: list) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["company", "category", "publishes_phone_number", "main_official_channel", "last_verified", "official_source_url"])
    for r in rows:
        writer.writerow([r["name"], r["category"], "yes" if r["phone_published"] else "no", r["channel"], r["verified"], r["source"]])
    return buf.getvalue()


def _summary_sentence(stats: dict) -> str:
    return (
        "Of the {total} well-known companies in the aicrazed directory, {no_phone} ({pct}%) do not publish "
        "a customer service phone number on their own websites. They send customers to live chat, contact "
        "forms, or help centers instead."
    ).format(**stats)


def _category_table(stats: dict, esc) -> str:
    rows = "".join(
        '<tr><th scope="row"><a href="/category/{slug}/">{label}</a></th><td>{total}</td><td>{has}</td><td>{no}</td></tr>'.format(
            slug=c["slug"], label=esc(c["label"]), total=c["total"], has=c["total"] - c["no_phone"], no=c["no_phone"]
        )
        for c in stats["by_cat"]
    )
    return """<div class="data-table-wrap"><table class="data-table">
<caption>Companies by category</caption>
<thead><tr><th scope="col">Category</th><th scope="col">Companies</th><th scope="col">Publish a phone number</th><th scope="col">No phone number</th></tr></thead>
<tbody>{rows}</tbody>
<tfoot><tr><th scope="row">All categories</th><td>{total}</td><td>{has}</td><td>{no}</td></tr></tfoot>
</table></div>""".format(rows=rows, total=stats["total"], has=stats["total"] - stats["no_phone"], no=stats["no_phone"])


def _company_table(rows: list, esc) -> str:
    body = "".join(
        """<tr><th scope="row"><a href="/brand/{slug}/">{name}</a></th><td>{cat}</td><td>{phone}</td><td>{channel}</td><td>{verified}</td><td><a href="{source}" rel="nofollow noopener" target="_blank">Official page</a></td></tr>""".format(
            slug=r["slug"],
            name=esc(r["name"]),
            cat=esc(r["category"]),
            phone="Yes" if r["phone_published"] else "<strong>No</strong>",
            channel=esc(r["channel"]),
            verified=esc(r["verified"]),
            source=esc(r["source"]),
        )
        for r in rows
    )
    return """<div class="data-table-wrap"><table class="data-table">
<caption>Every company in the directory</caption>
<thead><tr><th scope="col">Company</th><th scope="col">Category</th><th scope="col">Publishes a phone number?</th><th scope="col">Main official channel</th><th scope="col">Last verified</th><th scope="col">Source</th></tr></thead>
<tbody>{body}</tbody>
</table></div>""".format(body=body)


def report_faq(stats: dict, rows: list) -> list:
    no_phone_names = [r["name"] for r in rows if not r["phone_published"]]
    channels = ", ".join(
        "{} {}".format(n, label.lower()) for label, n in sorted(stats["no_phone_channels"].items(), key=lambda kv: -kv[1])
    )
    return [
        {
            "q": "How many major companies don't publish a customer service phone number?",
            "a": _summary_sentence(stats),
        },
        {
            "q": "Which companies don't publish a customer service phone number?",
            "a": "As of our most recent checks: " + ", ".join(no_phone_names) + ".",
        },
        {
            "q": "How do these companies handle support instead?",
            "a": "Among the companies with no published number, the main official channel is: {}.".format(channels),
        },
        {
            "q": "Is a phone number I found online for one of these companies real?",
            "a": "Treat it as unverified. If a company does not publish a number on its own website, a number shown in an ad, forum, or another directory is not confirmed and may belong to a scammer. Use the official channel linked on that company's aicrazed page.",
        },
    ]


def render_report(ctx: dict) -> str:
    """ctx carries the shared helpers from build.py: layout, esc, brands, categories, base_url, org_id."""
    esc, base_url = ctx["esc"], ctx["base_url"]
    rows = report_rows(ctx["brands"], ctx["categories"])
    stats = report_stats(rows, ctx["categories"])
    faq = report_faq(stats, rows)

    faq_html = "".join(
        '<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>'.format(q=esc(item["q"]), a=esc(item["a"]))
        for item in faq
    )
    body = """
<section class="page-hero container">
  <p class="breadcrumb" style="padding:0 0 12px;"><a href="/">Home</a> &rsaquo; Reports</p>
  <p class="eyebrow">Report &middot; listings verified {oldest} to {newest}</p>
  <h1>{title}</h1>
  <p class="lede" style="max-width:62ch;">{summary}</p>
</section>
<section class="section container">
  <div class="report-stats">
    <div class="report-stat"><span class="stat-value">{no_phone} of {total}</span><span class="stat-sub">companies publish no phone number</span></div>
    <div class="report-stat"><span class="stat-value">{pct}%</span><span class="stat-sub">of the directory is chat, form, or help-center only</span></div>
    <div class="report-stat"><span class="stat-value">{n_cats}</span><span class="stat-sub">categories covered</span></div>
  </div>

  <div class="prose" style="margin-top:40px;">
    <h2>By category</h2>
  </div>
  {cat_table}

  <div class="prose" style="margin-top:40px;">
    <h2>Company by company</h2>
    <p>Each row links to that company&rsquo;s full aicrazed listing and to the exact official page we checked. Companies with no published number are listed first.</p>
  </div>
  {company_table}
  <p class="stat-sub" style="margin-top:12px;"><a href="{csv_path}">Download this table as CSV</a></p>

  <div class="prose" style="margin-top:48px;">
    <h2>How this was measured</h2>
    <p>Each company&rsquo;s listing was checked directly against that company&rsquo;s own official help or contact page &mdash; never a forum, ad, or other directory. &ldquo;Publishes a phone number&rdquo; means a customer service number appears on the company&rsquo;s own site as page text. Companies that connect you by phone only after you sign in and choose an issue are counted as not publishing one, because there is no number a customer can verify in advance.</p>
    <p>Listings were last verified between {oldest} and {newest}; each row shows its own date. Companies change support channels without notice, so this page is regenerated whenever a listing is rechecked. The full standard is in our <a href="/editorial-policy/">Editorial Policy</a>.</p>

    <h2>Why it matters</h2>
    <p>When a company publishes no number, people search for one &mdash; and that gap is where fake &ldquo;support lines&rdquo; get placed in ads and spam pages. Knowing in advance that a company doesn&rsquo;t publish a number is the simplest protection: any number claiming to be theirs is unverified. See <a href="/how-it-works/">how to spot a fake support site</a>.</p>

    <h2>Citing this report</h2>
    <p>You&rsquo;re welcome to quote these figures. Please cite &ldquo;aicrazed, <em>{title_plain}</em>&rdquo; and link to <a href="{report_url}">{report_url}</a>. aicrazed is independent and not affiliated with any company listed.</p>
  </div>

  <div class="faq-list" style="margin-top:48px;border-top:1px solid var(--rule);">
    <h2 class="label-heading" style="margin:28px 0 4px;">Quick answers</h2>
    {faq_html}
  </div>
</section>
""".format(
        title=esc(REPORT_TITLE),
        title_plain=esc(REPORT_TITLE),
        summary=esc(_summary_sentence(stats)),
        no_phone=stats["no_phone"],
        total=stats["total"],
        pct=stats["pct"],
        n_cats=len(stats["by_cat"]),
        cat_table=_category_table(stats, esc),
        company_table=_company_table(rows, esc),
        csv_path=REPORT_CSV_PATH,
        oldest=esc(stats["oldest"]),
        newest=esc(stats["newest"]),
        report_url=base_url + REPORT_PATH,
        faq_html=faq_html,
    )

    page_url = base_url + REPORT_PATH
    dataset_ld = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": page_url + "#dataset",
        "name": REPORT_TITLE,
        "description": _summary_sentence(stats),
        "url": page_url,
        "dateModified": stats["newest"],
        "temporalCoverage": "{}/{}".format(stats["oldest"], stats["newest"]),
        "spatialCoverage": "United States",
        "creator": {"@id": ctx["org_id"]},
        "publisher": {"@id": ctx["org_id"]},
        "isAccessibleForFree": True,
        "variableMeasured": ["Publishes a customer service phone number", "Main official support channel", "Last verified date"],
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": base_url + REPORT_CSV_PATH}
        ],
    }
    webpage_ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": REPORT_TITLE,
        "url": page_url,
        "inLanguage": "en-US",
        "dateModified": stats["newest"],
        "isPartOf": {"@id": ctx["website_id"]},
        "publisher": {"@id": ctx["org_id"]},
        "mainEntity": {"@id": page_url + "#dataset"},
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faq
        ],
    }
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": base_url + "/"},
            {"@type": "ListItem", "position": 2, "name": "No phone support report", "item": page_url},
        ],
    }
    json_ld = "\n".join(
        '<script type="application/ld+json">{}</script>'.format(json.dumps(obj))
        for obj in (webpage_ld, dataset_ld, faq_ld, breadcrumb_ld)
    )
    return ctx["layout"](
        title="Companies With No Customer Service Phone Number ({} of {}) | aicrazed".format(
            stats["no_phone"], stats["total"]
        ),
        description="{} Verified against each company's own site; updated {}.".format(
            _summary_sentence(stats).split(". ")[0] + ".", stats["newest"]
        ),
        path=REPORT_PATH,
        body=body,
        json_ld=json_ld,
    )


def report_llms_lines(ctx: dict) -> list:
    rows = report_rows(ctx["brands"], ctx["categories"])
    stats = report_stats(rows, ctx["categories"])
    return [
        "## Reports",
        "",
        "- [{}]({}{}): {} CSV: {}{}".format(
            REPORT_TITLE, ctx["base_url"], REPORT_PATH, _summary_sentence(stats), ctx["base_url"], REPORT_CSV_PATH
        ),
        "",
    ]


def report_lastmod(ctx: dict) -> str:
    return max(b["verifiedDate"] for b in ctx["brands"])
