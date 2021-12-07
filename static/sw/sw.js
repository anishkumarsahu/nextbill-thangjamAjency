var version = 'v1.2.9::';
self.addEventListener("install", function (event) {
    console.log('WORKER: install event in progress.');
    event.waitUntil(
        caches
            .open(version + 'fundamentals')
            .then(function (cache) {
                return cache.addAll([
                '/static/logo/logo.png',
                '/static/cssMain/semantic.min.css',
                '/static/cssMain/dataTables.semanticui.min.css',
                '/static/cssMain/tableCss/dataTables.semanticui.min.css',
                '/static/cssMain/tableCss/buttons.semanticui.min.css',
                '/static/jsMain/jquery.min.js',
                '/static/jsMain/semantic.min.js',
                '/static/jsMain/jquery.dataTables.min.js',
                '/static/jsMain/dataTables.semanticui.min.js',
                '/static/table/dataTables.buttons.min.js',
                '/static/table/buttons.semanticui.min.js',
                '/static/table/jszip.min.js',
                '/static/table/pdfmake.min.js',
                '/static/table/buttons.html5.min.js',
                '/static/table/buttons.print.min.js',
                '/static/table/buttons.colVis.min.js',
                '/static/cssMain/themes/default/assets/fonts/brand-icons.woff2',
                'https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic&subset=latin'
                // 'https://fonts.gstatic.com/s/lato/v17/S6uyw4BMUTPHjx4wXiWtFCc.woff2'
                ]);
            })
            .then(function () {
                console.log('WORKER: install completed');
            })
    );
});
function get_url_extension( url ) {
    return url.split(/[#?]/)[0].split('.').pop().trim();
}
self.addEventListener("fetch", function (event) {
    console.log('WORKER: fetch event in progress.');
    if (event.request.method !== 'GET') {
        return;
    }
    event.respondWith(
        caches
            .match(event.request)
            .then(function (cached) {
                var networked = fetch(event.request)
                    .then(fetchedFromNetwork, unableToResolve)
                    .catch(unableToResolve);
                // console.log('WORKER: fetch event', cached ? '(cached)' : '(network)', event.request.url);
                return cached || networked;
                function fetchedFromNetwork(response) {
                    var cacheCopy = response.clone();
                    caches
                        .open(version + 'pages')
                        .then(function add(cache) {
                            var img =  get_url_extension(event.request.url);
                            if( img.toLowerCase() ==='png' || img.toLowerCase() ==='jpg' || img.toLowerCase() ==='jpeg'|| img.toLowerCase() ==='svg' ){
                             cache.put(event.request, cacheCopy);
                            }
                        })
                        .then(function () {
                            // console.log('WORKER: fetch response stored in cache.', event.request.url);
                        });
                    return response;
                }
                function unableToResolve() {
                    // console.log('WORKER: fetch request failed in both cache and network.');
                    return new Response('<h1>Service Unavailable</h1>', {
                        status: 503,
                        statusText: 'Service Unavailable',
                        headers: new Headers({
                            'Content-Type': 'text/html'
                        })
                    });
                }
            })
    );
});
self.addEventListener("activate", function (event) {
    console.log('WORKER: activate event in progress.');
    event.waitUntil(
        caches
            .keys()
            .then(function (keys) {
                return Promise.all(
                    keys
                        .filter(function (key) {
                            return !key.startsWith(version);
                        })
                        .map(function (key) {
                            return caches.delete(key);
                        })
                );
            })
            .then(function () {
                console.log('WORKER: activate completed.');
            })
    );
});


