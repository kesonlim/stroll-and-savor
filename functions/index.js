// Cloudflare Pages Function, matches the root route ("/") only.
//
// kfescapes.thethinkthank.com is a second custom domain on this same Pages
// project (stroll-and-savor) -- see site/scripts/build.py's "kfescapes
// landing alias" step and docs/growth-plan.md. Cloudflare Pages serves the
// identical static build to every custom domain attached to a project, so
// this function is what makes kfescapes.thethinkthank.com/ show the current
// month's KrisFlyer dashboard instead of the normal Stroll & Savor landing
// page, without duplicating any files or builds.
//
// Every other domain (strollsavor.thethinkthank.com, the .pages.dev URL)
// falls through via context.next() and gets the normal static landing.py
// output, unchanged.
export async function onRequest(context) {
  const host = context.request.headers.get("host") || "";
  if (host === "kfescapes.thethinkthank.com") {
    const url = new URL(context.request.url);
    url.pathname = "/_kfescapes-landing/";
    return context.env.ASSETS.fetch(new Request(url.toString(), context.request));
  }
  return context.next();
}
