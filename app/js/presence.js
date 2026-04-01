// ─── Presence Tracking System ───
// Dual-mode presence tracking:
//   1. Web Users — Server-side in-memory presence (POST /api/web/login, heartbeat, GET /api/web/users)
//   2. Server Users — Polls Linux server backend (/api/users via `who`)

const Presence = (function () {
    // ── Shared state ──
    let currentUser = '';
    let webUpdateCallbacks = [];
    let serverUpdateCallbacks = [];

    // ── Web Presence (server-backed) ──
    let webUsers = [];
    let sessionId = '';
    let heartbeatTimer = null;
    let webPollTimer = null;
    var HEARTBEAT_MS = 8000;       // heartbeat every 8s
    var WEB_POLL_MS = 5000;        // poll web users every 5s

    function generateSessionId() {
        return Date.now().toString(36) + '-' + Math.random().toString(36).substring(2, 9);
    }

    function serverUrl() {
        return (CONFIG.server && CONFIG.server.url) ? CONFIG.server.url.replace(/\/+$/, '') : '';
    }

    function authHeaders() {
        var h = { 'Content-Type': 'application/json' };
        var token = sessionStorage.getItem('authToken');
        if (token) h['Authorization'] = 'Bearer ' + token;
        return h;
    }

    function hasAuthenticatedSession() {
        return !!sessionStorage.getItem('authToken');
    }

    function initWeb() {
        sessionId = generateSessionId();
        var url = serverUrl();
        if (!url) {
            console.log('[Presence/Web] No server URL — web presence disabled.');
            return;
        }
        // Start polling web users immediately
        pollWebUsers();
        webPollTimer = setInterval(pollWebUsers, WEB_POLL_MS);

        // Clean up on tab close
        window.addEventListener('beforeunload', function () {
            if (currentUser && url) {
                // Use sendBeacon for reliable logout
                var data = JSON.stringify({ sessionId: sessionId });
                navigator.sendBeacon(url + '/api/web/logout', new Blob([data], { type: 'application/json' }));
            }
        });
    }

    function pollWebUsers() {
        var url = serverUrl();
        if (!url || !hasAuthenticatedSession()) {
            webUsers = [];
            notifyWeb();
            return;
        }
        fetch(url + '/api/web/users', { mode: 'cors', headers: authHeaders() })
            .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
            .then(function (data) {
                webUsers = (data.users || []).map(function (u) {
                    return {
                        name: u.name,
                        loginTime: u.loginTime || 0,
                        isSelf: u.sessionId === sessionId
                    };
                });
                // Sort: self first, then by login time
                webUsers.sort(function (a, b) {
                    if (a.isSelf && !b.isSelf) return -1;
                    if (!a.isSelf && b.isSelf) return 1;
                    return a.loginTime - b.loginTime;
                });
                notifyWeb();
            })
            .catch(function (err) {
                console.warn('[Presence/Web] Poll failed:', err.message);
            });
    }

    function webLogin(username) {
        var url = serverUrl();
        if (!url) return;
        fetch(url + '/api/web/login', {
            method: 'POST',
            mode: 'cors',
            headers: authHeaders(),
            body: JSON.stringify({ name: username, sessionId: sessionId })
        }).then(function () {
            pollWebUsers();
            // Start heartbeat
            if (heartbeatTimer) clearInterval(heartbeatTimer);
            heartbeatTimer = setInterval(function () {
                fetch(url + '/api/web/heartbeat', {
                    method: 'POST',
                    mode: 'cors',
                    headers: authHeaders(),
                    body: JSON.stringify({ sessionId: sessionId })
                }).catch(function () {});
            }, HEARTBEAT_MS);
        }).catch(function (err) {
            console.warn('[Presence/Web] Login failed:', err.message);
        });
    }

    function webLogout() {
        if (heartbeatTimer) { clearInterval(heartbeatTimer); heartbeatTimer = null; }
        var url = serverUrl();
        if (!url) return;
        fetch(url + '/api/web/logout', {
            method: 'POST',
            mode: 'cors',
            headers: authHeaders(),
            body: JSON.stringify({ sessionId: sessionId })
        }).then(function () { pollWebUsers(); })
            .catch(function () {});
    }

    function getWebUsers() { return webUsers; }

    function onWebUpdate(callback) { webUpdateCallbacks.push(callback); }
    function notifyWeb() { webUpdateCallbacks.forEach(function (cb) { cb(webUsers); }); }

    // ── Server Presence (Linux `who`) ──
    let serverUsers = [];
    let pollTimer = null;

    function initServer() {
        var url = serverUrl();
        if (!url) {
            console.log('[Presence/Server] No server URL configured.');
            return;
        }
        console.log('[Presence/Server] Polling', url);
        if (hasAuthenticatedSession()) pollServer();
        var interval = (CONFIG.server && CONFIG.server.pollInterval) || 10000;
        pollTimer = setInterval(pollServer, interval);
    }

    function pollServer() {
        var url = serverUrl();
        if (!url || !hasAuthenticatedSession()) {
            serverUsers = [];
            notifyServer();
            return;
        }
        fetch(serverUrl() + '/api/users', { mode: 'cors', headers: authHeaders() })
            .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
            .then(function (data) {
                serverUsers = data.users || [];
                notifyServer();
            })
            .catch(function (err) {
                console.warn('[Presence/Server] Poll failed:', err.message);
            });
    }

    function getServerUsers() {
        return serverUsers.map(function (u) {
            return {
                name: u.username,
                terminal: u.terminal || '',
                loginTime: u.loginTime || '',
                host: u.host || '',
                isSelf: currentUser && u.username.toLowerCase() === currentUser.toLowerCase()
            };
        }).sort(function (a, b) {
            if (a.isSelf && !b.isSelf) return -1;
            if (!a.isSelf && b.isSelf) return 1;
            return a.name.localeCompare(b.name);
        });
    }

    function onServerUpdate(callback) { serverUpdateCallbacks.push(callback); }
    function notifyServer() { var u = getServerUsers(); serverUpdateCallbacks.forEach(function (cb) { cb(u); }); }

    // ── Lifecycle ──
    function init() {
        initWeb();
        initServer();
    }

    function login(username) {
        currentUser = username;
        webLogin(username);
        if (hasAuthenticatedSession()) pollServer();
        else {
            webUsers = [];
            serverUsers = [];
            notifyWeb();
            notifyServer();
        }
    }

    function logout() {
        webLogout();
        currentUser = '';
        webUsers = [];
        serverUsers = [];
        notifyWeb();
        notifyServer();
    }

    function isLoggedIn() { return currentUser !== ''; }
    function getCurrentUser() { return currentUser; }

    window.addEventListener('beforeunload', function () {
        if (heartbeatTimer) clearInterval(heartbeatTimer);
        if (webPollTimer) clearInterval(webPollTimer);
        if (pollTimer) clearInterval(pollTimer);
    });

    return {
        init: init,
        login: login,
        logout: logout,
        isLoggedIn: isLoggedIn,
        getCurrentUser: getCurrentUser,
        // Web users (Firebase)
        getWebUsers: getWebUsers,
        getWebCount: function () { return getWebUsers().length; },
        onWebUpdate: onWebUpdate,
        // Server users (Linux)
        getServerUsers: getServerUsers,
        getServerCount: function () { return serverUsers.length; },
        onServerUpdate: onServerUpdate,
        refreshServer: pollServer
    };
})();
