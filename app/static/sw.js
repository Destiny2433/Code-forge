const CACHE = 'codeforge-shell-v2';
const SHELL = ['/static/css/app.css', '/static/js/app.js', '/static/manifest.json', '/static/icons/codeforge.svg', '/offline'];

self.addEventListener('install', event => {
	event.waitUntil(caches.open(CACHE).then(async cache => {
		await Promise.all(SHELL.map(async path => {
			try {
				const response = await fetch(path, { cache: 'reload' });
				if (response.ok) await cache.put(path, response);
			} catch (_) {
				// Keep installing when an optional shell resource is temporarily unavailable.
			}
		}));
	}));
	self.skipWaiting();
});

self.addEventListener('activate', event => {
	event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))));
	self.clients.claim();
});

self.addEventListener('fetch', event => {
	const request = event.request;
	const url = new URL(request.url);
	if (request.method !== 'GET' || url.origin !== self.location.origin) return;

	if (url.pathname.startsWith('/static/')) {
		event.respondWith(caches.match(request).then(cached => cached || fetch(request).then(response => {
			if (response.ok) caches.open(CACHE).then(cache => cache.put(request, response.clone()));
			return response;
		})));
		return;
	}

	const isPublicCoursePage = url.pathname === '/courses' || /^\/courses\/responsive-web-design(?:\/[^/]+)?\/?$/.test(url.pathname);
	if (!request.mode.includes('navigate') || !isPublicCoursePage) return;
	event.respondWith(fetch(request).then(response => {
		const cacheControl = response.headers.get('Cache-Control') || '';
		if (response.ok && response.headers.get('Content-Type')?.includes('text/html') && !/private|no-store/i.test(cacheControl)) {
			caches.open(CACHE).then(cache => cache.put(request, response.clone()));
		}
		return response;
	}).catch(async () => (await caches.match(request)) || (await caches.match('/offline'))));
});
