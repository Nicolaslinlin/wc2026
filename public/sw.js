// 2026 World Cup Predictor — Service Worker
// Strategy:
//   - HTML / our own files: network-first (always try fresh, cache as fallback)
//   - 3rd-party assets (twemoji, google fonts): cache-first (rarely change)
// Bumping VERSION evicts old caches.

const VERSION = 'wc2026-v2';
const SHELL = ['./', './index.html', './icon.svg', './manifest.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  const sameOrigin = url.origin === self.location.origin;
  const isCacheableThirdParty =
    url.hostname === 'unpkg.com' ||
    url.hostname === 'fonts.googleapis.com' ||
    url.hostname === 'fonts.gstatic.com' ||
    url.hostname === 'twemoji.maxcdn.com';

  if (sameOrigin) {
    // network-first for our own files (so users always see fresh predictions when online)
    event.respondWith(
      fetch(event.request)
        .then(resp => {
          const clone = resp.clone();
          caches.open(VERSION).then(c => c.put(event.request, clone)).catch(() => {});
          return resp;
        })
        .catch(() => caches.match(event.request))
    );
  } else if (isCacheableThirdParty) {
    // cache-first for static 3rd-party assets
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(resp => {
          const clone = resp.clone();
          caches.open(VERSION).then(c => c.put(event.request, clone)).catch(() => {});
          return resp;
        });
      })
    );
  }
  // everything else (e.g. analytics) passes through untouched
});
