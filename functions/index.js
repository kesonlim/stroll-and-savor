// Cloudflare Pages Function, matches the root route ("/") only.
//
// 1. 301 Redirect old thethinkthank.com domains to strollsavor.com:
//    - kfescapes.thethinkthank.com -> https://strollsavor.com/kfescapes/
//    - strollsavor.thethinkthank.com -> https://strollsavor.com/...
// 2. Normal strollsavor.com requests fall through to static assets.

export async function onRequest(context) {
  const host = context.request.headers.get("host") || "";
  const url = new URL(context.request.url);

  // 301 redirect kfescapes.thethinkthank.com to strollsavor.com/kfescapes/
  if (host === "kfescapes.thethinkthank.com") {
    return Response.redirect("https://strollsavor.com/kfescapes/", 301);
  }

  // 301 redirect old strollsavor subdomain to root domain
  if (host === "strollsavor.thethinkthank.com") {
    return Response.redirect(`https://strollsavor.com${url.pathname}${url.search}`, 301);
  }

  return context.next();
}
