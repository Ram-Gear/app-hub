/* Ram-Gear Shop Apps: service worker.
   Caches the hub shell so the launcher opens offline.
   - index.html / navigations: network-first (updates show up), cached copy when offline.
   - Other shell files (manifest, icons): stale-while-revalidate.
   - Anything cross-origin or outside this folder (the apps themselves) is NOT intercepted.
   Bump VERSION when the list of shell files changes. */
const VERSION = "rg-hub-v1";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/app-hub.svg",
  "./icons/app-hub-64.png",
  "./icons/app-hub-192.png",
  "./icons/app-hub-512.png",
  "./icons/qc-form.svg",
  "./icons/web-gear-calc.svg",
  "./icons/rg-worm-mow.svg",
  "./icons/cardfile.svg",
  "./icons/change-gear.svg",
];
const SCOPE = new URL("./", self.location).href;

self.addEventListener("install", event => {
  event.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith("rg-hub-") && k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET" || !req.url.startsWith(SCOPE)) return; // leave external apps alone

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then(res => {
          if (res.ok) { const copy = res.clone(); caches.open(VERSION).then(c => c.put("./index.html", copy)); }
          return res;
        })
        .catch(() => caches.match("./index.html").then(r => r || caches.match("./")))
    );
    return;
  }

  event.respondWith(
    caches.open(VERSION).then(cache =>
      cache.match(req).then(cached => {
        const network = fetch(req)
          .then(res => { if (res.ok) cache.put(req, res.clone()); return res; })
          .catch(() => cached);
        return cached || network;
      })
    )
  );
});
