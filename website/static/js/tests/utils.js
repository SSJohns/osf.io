'use strict';
var assign = require('object-assign');
// var sinon = window.sinon || require('sinon');

/**
 * Utility to create a fake server with sinon.
 *
 * See http://sinonjs.org/docs/#fakeServer
 *
 * Example:
 *
 * var server;
 * before(() => {
 *     server = createServer(sinon, [
 *        {url: '/projects/':  method: 'GET', response: {'id': '12345'}}
 *        {url: '/projects/': method: 'POST',
 *          response: {message: 'Successfully created project.'}, status: 201}
 *        {url: /\/project\/(\d+)/, method: 'GET',
 *          response: {message: 'Got single project.'}}
 *     ]);
 * });
 *
 * after(() => { server.restore(); });
 */
var defaultHeaders = {'Content-Type': 'application/json'};
function createServer(sinon, endpoints) {
    var server = sinon.fakeServer.create();
    endpoints.forEach(function(endpoint) {
        var headers = assign(
            {},
            defaultHeaders,
            endpoints.headers
        );
        server.respondWith(
            endpoint.method || 'GET',
            endpoint.url,
            [
                endpoint.status || 200,
                headers,
                JSON.stringify(endpoint.response)
            ]
        );
    });
    return server;
}

module.exports = {
    createServer: createServer
};
