const CACHE = "events_v1";

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE).then(cache => cache.addAll([
            "/templates/events.html",
            "/static/style.css",
            "/static/manifest.json",
            "/static/192x192.png",
            "/static/512x512.png"
        ]))
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(r => r || fetch(event.request))
    );
});