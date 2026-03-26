// ─── Presence Tracking System ───
// Dual-mode presence tracking:
//   1. Web Users — Firebase Realtime Database (visitors browsing the site)
//   2. Server Users — Polls Linux server backend (/api/users via `who`)

const Presence = (function () {
    // ── Shared state ──
    let currentUser = '';
    let webUpdateCallbacks = [];
    let serverUpdateCallbacks = [];

    // ── Web Presence (Firebase) ──
    let webUsers = {};          // { key: { name, loginTime, sessionId } }
    let myPresenceRef = null;
    let presenceRef = null;
    let firebaseReady = false;
    let sessionId = '';

    function generateSessionId() {
        return Date.now().toString(36) + '-' + Math.random().toString(36).substring(2, 9);
    }

    function initFirebase() {
        sessionId = generateSessionId();
        if (!CONFIG.firebase || !CONFIG.firebase.enabled || !CONFIG.firebase.databaseURL) {
            console.log('[Presence/Web] Firebase not configured.');
            return;
        }
        try {
            if (typeof firebase === 'undefined') {
                console.warn('[Presence/Web] Firebase SDK not loaded.');
                return;
            }
            if (!firebase.apps.length) {
                firebase.initializeApp({
                    apiKey: CONFIG.firebase.apiKey,
                    authDomain: CONFIG.firebase.authDomain,
                    databaseURL: CONFIG.firebase.databaseURL,
                    projectId: CONFIG.firebase.projectId
                });
            }
            presenceRef = firebase.database().ref('presence');
            firebaseReady = true;
            console.log('[Presence/Web] Firebase connected.');
            presenceRef.on('value', function (snapshot) {
                webUsers = snapshot.val() || {};
                notifyWeb();
            });
        } catch (err) {
            console.warn('[Presence/Web] Firebase init failed:', err.message);
        }
    }

    function webLogin(username) {
        var entry = { name: username, loginTime: Date.now(), sessionId: sessionId };
        if (firebaseReady && presenceRef) {
            myPresenceRef = presenceRef.push();
            myPresenceRef.set(entry);
            myPresenceRef.onDisconnect().remove();
        } else {
            webUsers[sessionId] = entry;
            notifyWeb();
        }
    }

    function webLogout() {
        if (firebaseReady && myPresenceRef) {
            myPresenceRef.remove();
            myPresenceRef = null;
        } else {
            delete webUsers[sessionId];
            notifyWeb();
        }
    }

    function getWebUsers() {
        var users = [];
        var seen = new Set();
        Object.keys(webUsers).forEach(function (key) {
            var u = webUsers[key];
            if (u && u.name) {
                var ident = u.name + '|' + (u.sessionId || key);
                if (!seen.has(ident)) {
                    seen.add(ident);
                    users.push({
                        name: u.name,
                        loginTime: u.loginTime || 0,
                        isSelf: u.sessionId === sessionId
                    });
                }
            }
        });
        users.sort(function (a, b) {
            if (a.isSelf && !b.isSelf) return -1;
            if (!a.isSelf && b.isSelf) return 1;
            return a.loginTime - b.loginTime;
        });
        return users;
    }

    function onWebUpdate(callback) { webUpdateCallbacks.push(callback); }
    function notifyWeb() { var u = getWebUsers(); webUpdateCallbacks.forEach(function (cb) { cb(u); }); }

    // ── Server Presence (Linux `who`) ──
    let serverUsers = [];       // [{ username, terminal, loginTime, host }]
    let pollTimer = null;
    let serverUrl = '';

    function initServer() {
        serverUrl = (CONFIG.server && CONFIG.server.url) ? CONFIG.server.url.replace(/\/+$/, '') : '';
        if (!serverUrl) {
            console.log('[Presence/Server] No server URL configured.');
            return;
        }
        console.log('[Presence/Server] Polling', serverUrl);
        pollServer();
        var interval = (CONFIG.server && CONFIG.server.pollInterval) || 10000;
        pollTimer = setInterval(pollServer, interval);
    }

    function pollServer() {
        if (!serverUrl) return;
        fetch(serverUrl + '/api/users', { mode: 'cors' })
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
        initFirebase();
        initServer();
    }

    function login(username) {
        currentUser = username;
        webLogin(username);
        pollServer();
    }

    function logout() {
        webLogout();
        currentUser = '';
    }

    function isLoggedIn() { return currentUser !== ''; }
    function getCurrentUser() { return currentUser; }

    window.addEventListener('beforeunload', function () {
        webLogout();
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
