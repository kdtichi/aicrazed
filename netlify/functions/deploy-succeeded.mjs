// Netlify event-triggered function: runs automatically after every successful
// deploy (the file name is the trigger). On production deploys it tells
// IndexNow-participating search engines (Bing, Yandex, Seznam, Naver, Yep) that
// the site's URLs changed, so they recrawl within hours instead of days. Bing's
// index feeds ChatGPT search and Copilot, so this is the fast path into AI answers.
//
// The IndexNow key is public by design: the same value is served at
// https://aicrazed.com/<key>.txt so engines can confirm we own the host.

const HOST = "aicrazed.com";
const KEY = "0ef2521de73a52e8c6d8c1533b420460";
const ENDPOINT = "https://api.indexnow.org/indexnow";
const MAX_URLS = 10000; // IndexNow's per-request limit

function urlsFromSitemap(xml) {
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)]
    .map((m) => m[1].trim())
    .filter((u) => new URL(u).host === HOST)
    .slice(0, MAX_URLS);
}

export const handler = async (event) => {
  let context = "";
  try {
    context = JSON.parse(event.body || "{}").payload?.context || "";
  } catch {
    console.error("IndexNow: could not parse deploy payload; skipping");
    return { statusCode: 200, body: "skipped: bad payload" };
  }
  if (context !== "production") {
    return { statusCode: 200, body: `skipped: ${context || "unknown"} deploy` };
  }

  try {
    const sitemap = await fetch(`https://${HOST}/sitemap.xml`);
    if (!sitemap.ok) throw new Error(`sitemap HTTP ${sitemap.status}`);
    const urlList = urlsFromSitemap(await sitemap.text());
    if (urlList.length === 0) throw new Error("sitemap had no URLs");

    const res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json; charset=utf-8" },
      body: JSON.stringify({ host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList }),
    });
    // 200 = accepted, 202 = accepted pending key check; anything else is worth seeing in the function log.
    console.log(`IndexNow: submitted ${urlList.length} URLs, HTTP ${res.status}`);
    return { statusCode: 200, body: `submitted ${urlList.length} URLs (${res.status})` };
  } catch (err) {
    // Never fail loudly: a missed ping just means engines find changes on their normal crawl.
    console.error(`IndexNow: ${err.message}`);
    return { statusCode: 200, body: `error: ${err.message}` };
  }
};
