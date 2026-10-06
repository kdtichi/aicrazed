# Paid advertising compliance research

Internal reference document, not published on the live site. Records what was actually verified about running paid ads for aicrazed on Google Ads and Microsoft Advertising, so this doesn't get re-litigated from scratch later. Findings are dated — ad network policies change; re-verify before relying on anything here after a few months.

## The short version

- **Microsoft Advertising: paid ads for this business model are categorically prohibited, with no appeal.** This is not fixable by better disclosures or ad copy. Do not spend budget trying.
- **Google Ads: likely also blocked for this business model, confirmed by an actual disapproval — see the 2026-10-01 correction below.** A real pilot campaign (UPS + DoorDash, both "lowest risk" brands) was disapproved for "restricted product or service," matching Google's own policy listing for "Call directory, forwarding, and recording services" as flatly prohibited. Brand selection and ad copy quality did not prevent this. Do not assume a different brand or better copy fixes it without a confirmed answer from Google support first.
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

### Update 2026-10-01: tiering for the 13 brands added this session (shipping/airlines/rideshare/insurance)

Applying the same two criteria (real published phone number; not an account-recovery/scam-pattern category or aggressive-trademark brand) to the new additions:

**Lowest risk, recommended for the first campaign:** Insurance (GEICO, State Farm, Allstate) and Shipping (UPS, FedEx, USPS) — all six have real phone numbers, none are tech-support-adjacent, and none of these companies have the aggressive third-party-ad trademark-enforcement posture that Amazon/Meta/Netflix/Apple have. This is exactly why these verticals were chosen when expanding the site in the first place. Top pick for the actual first page to run: **GEICO or UPS.**

**Second tier, still low risk:** Airlines (Delta, American, United, Southwest) — same profile, marginally more consumer-complaint volume around flight disruptions than insurance/shipping, worth a second wave rather than the pilot.

**Exclude from paid ads regardless of category:** Uber and Lyft — neither publishes any phone number (confirmed via direct research against their own official sites), which undercuts the ad's core value proposition and will likely hurt Quality Score/approval odds independent of category risk. Fine for organic SEO, not recommended for paid.

### Update 2026-10-01 (correction): likely categorical prohibition, not just brand-tier risk

**What happened:** A real pilot campaign was built (UPS + DoorDash ad groups — both in the "lowest risk" tier above) and both ad groups were disapproved with: *"Your ads relate to a restricted product or service. In order for your ads to start running, you'll need to apply for specific approval."*

**Re-verified directly against Google's own policy page** (https://support.google.com/adspolicy/answer/6368711, fetched twice independently for exact wording): the "Other restricted businesses" page lists **"Call directory, forwarding, and recording services"** as prohibited — exact quote: *"Promotions for call directory, forwarding, and recording services are not allowed."* — shown with a red X (no certification pathway), the same tier as "Third-party consumer technical support" (*"Technical support for consumer technology products and online services provided by third-party providers is not allowed"*).

**Why this matters:** aicrazed.com is, functionally, a directory of companies' call/contact information. That both UPS and DoorDash — brands with no trademark-enforcement red flags, both with real published phone numbers, neither in a scam-pattern category — were disapproved identically suggests the block may be on the **business model itself** (being a "call directory"), not brand-specific trademark/scam-pattern risk as the brand-tiering above assumed. If that's correct, no brand selection or ad-copy change fixes this — it would mean Google Ads, like Microsoft Advertising, effectively blocks this business model, just with less explicit language about it ("restricted" + an inapplicable-in-practice "apply for approval" prompt, rather than Microsoft's flat "no appeal" statement).

**Not yet fully confirmed:** this is read from Google's policy page and one real disapproval, not a definitive answer from Google support. It's possible a manual policy appeal clarifies the line differently (e.g. a plain informational page listing a publicly available number might be judged differently from an active call-forwarding/routing service) — that would need an actual appeal response to know for sure, not further inference from the policy page.

**Practical conclusion (supersedes the "narrow pilot is plausible" conclusion above):** do not spend further budget assuming the brand-tiering alone will get a campaign approved. Before any further paid Google Ads spend: either (a) file Google's policy appeal with support and get a specific human answer about whether this business model qualifies, or (b) treat Google Ads as likely closed for this business model, same as Microsoft, and rely on organic SEO only (unaffected by either ad policy).

### Update 2026-10-06: Google Ads account suspended (Unacceptable business practices)

**What happened:** The Google Ads account (customer 666-734-5000, "Ai Crazed") was reported suspended for violating the **Unacceptable business practices** policy, after the UPS & DoorDash pilot campaign had run for a few days. Google's exact sub-reason is shown in the account notification and has not been recorded here yet — capture it before appealing.

**What Google's own pages say** (support.google.com/adspolicy/answer/15938071 and support.google.com/google-ads/answer/9841640, fetched 2026-10-06):
- The policy covers making it seem like you're affiliated with another brand, and impersonating brands or businesses. Violations are treated as egregious: suspension "upon detection and without prior warning," and "you will not be allowed to advertise with Google Ads again."
- "Accounts are only reinstated in compelling circumstances, and when there is good reason."
- Any new account the advertiser tries to create "may also be suspended." Do not open a replacement account.
- Appeals go through the Contact Us link in the account notification. One appeal at a time; too many appeals for one suspension may be ignored, and misuse can pause appeal processing for 7 days.

**Where the pilot departed from the brand guardrails (skill `aicrazed-brand`), which had not been loaded when the campaign was built:**
- Phase 1 was specified as Temu + Shein; the pilot used UPS + DoorDash.
- Ad text put brand names next to support-line wording ("UPS Customer Service Number", "UPS Customer Care Number", "DoorDash Customer Care") and one description said "Tap to call UPS directly" — the guardrails forbid the brand name next to "call", "support line", or "helpline".
- Independence wording was in descriptions only; a responsive search ad can show headlines without it, so no single impression was guaranteed to carry it.
- All keywords were broad match; the guardrails require phrase/exact for brand terms.
- Site side: brand-page meta/og descriptions read "Official {brand} customer service: ..." (build.py, render_brand), which contradicts the independent-directory positioning on the landing page itself.

Which of these, if any, Google actually acted on is unknown. This list is what a careful reviewer could object to, not a finding of cause.

**Practical conclusion:** treat Google Ads as unavailable for now. Do not create new accounts. At most one carefully written appeal after the site/copy issues above are fixed and the exact reason is known. Organic SEO is unaffected.
