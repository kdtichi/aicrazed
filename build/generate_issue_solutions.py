"""
One-off helper that bulk-generates {"issue", "solution"} pairs for commonIssues
by keyword-categorizing each issue string and filling in a generic, safe
solution template. It was used once to migrate every brand's commonIssues
from plain strings to {issue, solution} objects — kept here so the same
categorize()/solution_for() logic can be reused (e.g. via ToolSearch import,
or copy the two functions) when adding a new brand's issues by hand, rather
than writing ad hoc solution text each time.

Deliberately NOT meant to be re-run as-is against the live brands.json: it
expects commonIssues to still be a list of plain strings, and will crash
(brand["commonIssues"].append on a dict, or similar) if run against data
that's already been migrated. If you do want to bulk-process new entries,
either restore a pre-migration copy first or adapt the loop at the bottom to
only touch string entries.

Every "solution" here is deliberately generic and brand-agnostic beyond
inserting the brand's own name — never a specific policy, refund window, or
procedure that hasn't actually been verified for that company. See the
README's "Adding or editing a brand" section for why that line matters.
"""
import json

PATH = "/Users/rameezjamal/Downloads/claude/data/brands.json"
data = json.load(open(PATH))

ADDITIONS = {
    "instagram": "Report a fake or impersonating account",
    "x": "Report abusive or harmful content",
    "tiktok": "Report inappropriate content",
    "snapchat": "Deactivate or delete your account",
    "pinterest": "Report inappropriate pins or content",
    "spotify": "Cancel or change your subscription",
}

# Order matters: more specific / higher-signal keywords first.
RULES = [
    ("security_fraud_dispute", ["fraud", "dispute", "security concern"]),
    ("cancel_order", ["cancel an order", "cancel order", "edit or cancel"]),
    ("returns_refunds", ["return", "refund"]),
    ("apple_backup_sync", ["icloud drive", "icloud keychain", "back up or restore", "manage icloud"]),
    ("email_sync_delivery", ["messages are missing", "bounced", "sync and import", "unwanted or suspicious", "emails not received", "pop/imap", "spam"]),
    ("order_tracking", ["order", "shipment", "shipping", "delivery", "tracking"]),
    ("hacked_compromised", ["hack", "compromise", "compromised"]),
    ("locked_suspended", ["locked", "suspended", "disabled", "under review"]),
    ("account_deletion", ["reactivate or close", "deactivate or delete"]),
    ("login_access", ["login", "log in", "sign-in", "sign in", "password", "account access", "account recovery", "account basics"]),
    ("account_management_general", ["data and privacy"]),
    ("report_safety", ["report", "safety", "privacy", "rules and reporting", "community guidelines", "authenticity", "impersonation", "abusive"]),
    ("billing_payment", ["billing", "payment", "pricing", "promo", "gift card", "giftcard"]),
    ("membership_subscription", ["membership", "subscription", "premium plan", "plan changes", "add-ons", "dashpass"]),
    ("device_technical", ["sim", "esim", "unlock a device"]),
    ("connection_network", ["connection", "network", "voicemail"]),
    ("playback_streaming", ["playback", "streaming"]),
    ("tax_documents", ["tax document"]),
    ("price_match", ["price match"]),
    ("product_repair", ["product repair"]),
    ("store_pickup", ["pickup", "store pickup"]),
    ("international_service", ["international"]),
    ("marketplace_groups", ["marketplace", "groups and pages"]),
    ("productivity_features", ["calendar", "people and profiles", "share and delegate", "job search", "contacts", "custom email domain", "addresses and identities", "using proton mail", "using hulu"]),
    ("getting_started", ["getting started", "get started"]),
    ("account_management_general", ["managing", "account settings", "account and payment", "profile", "account issues", "account status", "data and privacy", "features and experiences"]),
]

def categorize(issue):
    low = issue.lower()
    for cat, keywords in RULES:
        for kw in keywords:
            if kw in low:
                return cat
    return "fallback"

def solution_for(cat, brand):
    b = brand
    T = {
        "order_tracking": "Have your order number and the email used at checkout ready before you reach out — most order-status questions are resolved fastest with those on hand, using the contact option above.",
        "cancel_order": f"Check your order history first — many orders can still be canceled there if it hasn't shipped yet. If that option is gone, contact {b} above as soon as possible; the sooner you ask, the better the odds of stopping it.",
        "returns_refunds": "Start a return from your order history if possible, and keep your receipt or order confirmation handy. If the order doesn't show a return option, use the contact channel above instead.",
        "login_access": f"Try {b}'s own password reset link first — it resolves most sign-in issues faster than contacting support. If you no longer have access to the recovery email or phone number on file, use the option above and be ready to prove account ownership another way.",
        "hacked_compromised": "Change your password immediately from a device you trust, then report it using the contact option above. Don't trust any other phone number or link claiming to help “recover” your account.",
        "locked_suspended": f"Check your email for a message from {b} explaining the suspension — it usually states the reason and next step. If you don't see one, use the option above to ask directly.",
        "account_deletion": "This is usually handled directly in your account settings without needing to contact support. Use the contact option above only if the in-app option isn't working, or to recover a recently closed account.",
        "report_safety": "Use the in-app or on-page reporting tool first — it's usually faster than general support for this. Use the contact option above if there's no direct reporting flow for your situation.",
        "billing_payment": f"Double-check the card or payment method on file for a typo or expiration date first. If a charge still looks wrong, contact {b} above with the exact date and amount.",
        "membership_subscription": f"Manage or cancel your plan directly in your account settings — changes usually apply immediately there. Contact {b} above if the option isn't available or a charge doesn't match your plan.",
        "device_technical": f"Restart the device and reseat the SIM first, since that resolves a lot of these on its own. If it doesn't, contact {b} above with your device model and account number ready.",
        "connection_network": f"Check for a reported service outage in your area before assuming it's your device or account. If nothing's reported, contact {b} above.",
        "playback_streaming": f"Restart the app and your device, and confirm your internet connection is stable — that fixes most playback issues. Contact {b} above if it persists, with the device and error message you're seeing.",
        "email_sync_delivery": f"Check your spam or junk folder and any mail filters first, since misdirected or delayed mail is the most common cause. Contact {b} above if the message still doesn't turn up.",
        "apple_backup_sync": "Check your device's iCloud settings and available storage first, since that's the most common cause. Use the contact option above if the sync or backup issue continues.",
        "tax_documents": f"Tax documents are usually posted to your account's statements or documents section by a set date. Contact {b} above if yours is missing after that.",
        "security_fraud_dispute": f"Contact {b} above as soon as you notice it — the sooner a disputed charge or security concern is reported, the more options they have to fix it.",
        "price_match": f"Have your receipt and a link or ad showing the lower price ready — most price-match requests need both. Contact {b} above to submit it.",
        "product_repair": f"Check whether your item is still under warranty first, since that changes what {b} can offer. Contact them above with your order or serial number.",
        "store_pickup": f"Confirm your pickup-ready notification, and bring the order confirmation and ID used at checkout. Contact {b} above if the order isn't ready when expected.",
        "international_service": "Check the help center linked above for country-specific requirements before you travel or reach out — international terms often differ from domestic ones.",
        "marketplace_groups": f"These are managed through their own dedicated settings inside the app rather than general account settings. {b}'s help center above covers the specific controls.",
        "productivity_features": f"This is a feature-configuration question rather than an account problem — {b}'s help center above walks through the exact steps. Contact them directly if you get stuck partway through.",
        "getting_started": f"{b}'s own help center covers most setup questions step by step, which is usually faster than contacting support directly. Use the option above if your situation isn't addressed there.",
        "account_management_general": f"Most account details can be updated directly in your account settings. Contact {b} above for anything the settings page doesn't cover.",
        "fallback": f"Have your account details and a clear description of the issue ready, then use the contact option above — that's the fastest way to get this resolved directly with {b}.",
    }
    return T[cat]

for brand in data["brands"]:
    if brand["slug"] in ADDITIONS:
        brand["commonIssues"].append(ADDITIONS[brand["slug"]])
    brand["commonIssues"] = [
        {"issue": issue, "solution": solution_for(categorize(issue), brand["name"])}
        for issue in brand["commonIssues"]
    ]

json.dump(data, open(PATH, "w"), indent=2, ensure_ascii=False)
open(PATH, "a").write("\n")
print("done")
