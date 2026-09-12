# Paid advertising compliance research

Internal reference document, not published on the live site. Records what was actually verified about running paid ads for aicrazed on Google Ads and Microsoft Advertising, so this doesn't get re-litigated from scratch later. Findings are dated — ad network policies change; re-verify before relying on anything here after a few months.

## The short version

- **Microsoft Advertising: paid ads for this business model are categorically prohibited, with no appeal.** This is not fixable by better disclosures or ad copy. Do not spend budget trying.
- **Google Ads: not prohibited outright, but heavily scrutinized.** A narrower set of brands (real published phone numbers, non-scam-associated categories) has a realistic shot at approval with careful, honest ad copy. Expect friction and some disapprovals as normal, not a sign of a broken account.
- **Neither policy affects organic search.** Both are paid-advertising rules. aicrazed can rank normally in unpaid Google and Bing search results regardless.

---

## Microsoft Advertising

**Researched:** 2026-09-12, via web search and direct fetch of Microsoft's own policy/support pages.

Microsoft Advertising's Misleading Content policy, under "Promotion of third-party products and services," states (quoted verbatim from a Microsoft Q&A thread citing the actual disapproval policy text):

> "Advertisers may not promote online technical support to consumers for products or services that the advertisers do not directly own."

This is explicitly stated to cover **all technical support offerings**, with:

> "There is no appeal for this decision."

and

> "We may again in the future reconsider these policies, however at this time we are unable to offer services to companies offering support for products that they do not own."

### What this means for aicrazed specifically

aicrazed's core business — surfacing customer service/support contact information for companies it doesn't own or operate — is exactly the category this policy targets. There is no version of "better disclosure" or "clearer independence language" that changes this: the policy blocks the *category*, not specific deceptive executions of it. This is a materially different (and stricter) posture than Google Ads, which restricts trademark usage in ad copy but doesn't categorically ban the business model.

**Practical conclusion:** don't build or fund a Microsoft Advertising campaign for aicrazed's core listings. If Microsoft revises this policy in the future (their own text leaves that door open), re-verify before revisiting.

### What's unaffected

This is a paid-advertising-only restriction. It does not touch:
- Organic Bing search ranking (unaffected — same SEO fundamentals as Google: schema, sitemap, `llms.txt`, page speed, content quality)
- Bing Webmaster Tools / IndexNow submission
- Any non-Microsoft ad network

**Sources:**
- [Ads Disapproved — Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/6f1f9995-d88d-4956-a9bb-4fa65cad5807/ads-disapproved?forum=msadvs-msadvs_ads-msadvs_editpolguid) — direct quote of the policy and "no appeal" language
- [Introduction to Microsoft Advertising Network policies](https://about.ads.microsoft.com/en-us/policies/home)
- [Intellectual property policies — Microsoft Advertising](https://about.ads.microsoft.com/en-us/policies/intellectual-property-policies)

---

## Google Ads

**Researched:** earlier session, general knowledge + established Google Ads trademark/policy patterns for this niche (not re-verified via live fetch on this pass — treat as somewhat less current than the Microsoft findings above).

Google does not categorically ban third-party support directories, but:

- **Trademark policy**: bidding on brand keywords ("netflix customer service") is generally fine; using the trademark in the *visible ad text/headline* is where Google's trademark-complaint process bites, especially for brands with active legal/brand-protection teams (Amazon, Meta, Netflix, Apple).
- **Anti-scam enforcement**: "fake customer service number" is a well-known, heavily automated-and-manually-reviewed abuse pattern. Expect extra scrutiny and some disapprovals purely for being in this category, independent of how honest the actual ad is.
- **Landing page requirements**: clear business identity, real privacy policy, working site — aicrazed already satisfies these.

### Brand tiering used for the first ad-group draft

Lower risk (real published phone numbers, not associated with account-takeover scam patterns): DoorDash, Walmart, Target, Shein, Verizon, AT&T, T-Mobile — retail order-support and telecom billing-support queries are a comparatively boring, legitimate ad category.

Higher risk, deliberately excluded from the first batch: Amazon, Facebook, Instagram, Netflix, iCloud (aggressive trademark enforcement and/or no real phone number on our page, which also hurts Quality Score), plus the entire social-media and email-provider verticals (account-recovery queries are the single biggest scam-ad pattern Google's reviewers train on).

**Practical conclusion:** a narrow, careful Google Ads pilot on the lower-risk tier is plausible. Full account-wide advertising across all 28 brands is not recommended even where technically not prohibited — the risk/reward gets worse as you move into the higher-risk tier.

**Recommended before spending any budget:** re-verify current Google Ads policy directly (policy pages change), and read the actual current text of the trademark and "unacceptable business practices" policies rather than relying on this summary.
