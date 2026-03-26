// ─── Presence Tracking System ───
// Tracks who is currently logged in and displays online users.
// Uses Firebase Realtime Database when configured, otherwise falls back to local-only mode.

const Presence = (function () {
    let currentUser = '';
    let onlineUsers = {};       // { uniqueKey: { name, loginTime } }
    let myPresenceRef = null;
    let presenceRef = null;
    let firebaseReady = false;
    let sessionId = '';
    let updateCallbacks = [];

    // Generate a unique session ID
    function generateSessionId() {
        return Date.now().toString(36) + '-' + Math.random().toString(36).substring(2, 9);
    }

    // Initialize Firebase if configured
    function init() {
        sessionId = generateSessionId();

        if (!CONFIG.firebase.enabled || !CONFIG.firebase.databaseURL) {
            console.log('[Presence] Firebase not configured — running in local-only mode.');
            return;
        }

        try {
            if (typeof firebase === 'undefined') {
                console.warn('[Presence] Firebase SDK not loaded.');
                return;
            }

            // Initialize Firebase if not already done
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
            console.log('[Presence] Firebase connected.');

            // Listen for changes to the online users list
            presenceRef.on('value', function (snapshot) {
                onlineUsers = snapshot.val() || {};
                notifyUpdate();
            });
        } catch (err) {
            console.warn('[Presence] Firebase init failed:', err.message);
        }
    }

    // Register a user's presence
    function login(username) {
        currentUser = username;
        const entry = {
            name: username,
            loginTime: Date.now(),
            sessionId: sessionId
        };

        if (firebaseReady && presenceRef) {
            // Push presence to Firebase
            myPresenceRef = presenceRef.push();
            myPresenceRef.set(entry);

            // Remove on disconnect
            myPresenceRef.onDisconnect().remove();
        } else {
            // Local-only: just track ourselves
            onlineUsers[sessionId] = entry;
            notifyUpdate();
        }
    }

    // Remove user's presence (on logout or page unload)
    function logout() {
        if (firebaseReady && myPresenceRef) {
            myPresenceRef.remove();
            myPresenceRef = null;
        } else {
            delete onlineUsers[sessionId];
            notifyUpdate();
        }
        currentUser = '';
    }

    // Get list of online users
    function getOnlineUsers() {
        const users = [];
        const seen = new Set();
        Object.keys(onlineUsers).forEach(function (key) {
            const u = onlineUsers[key];
            if (u && u.name) {
                // Deduplicate by name+sessionId
                const ident = u.name + '|' + (u.sessionId || key);
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
        // Sort: self first, then by login time
        users.sort(function (a, b) {
            if (a.isSelf && !b.isSelf) return -1;
            if (!a.isSelf && b.isSelf) return 1;
            return a.loginTime - b.loginTime;
        });
        return users;
    }

    function getOnlineCount() {
        return getOnlineUsers().length;
    }

    function getCurrentUser() {
        return currentUser;
    }

    function isLoggedIn() {
        return currentUser !== '';
    }

    // Register callback for when online users change
    function onUpdate(callback) {
        updateCallbacks.push(callback);
    }

    function notifyUpdate() {
        updateCallbacks.forEach(function (cb) { cb(getOnlineUsers()); });
    }

    // Clean up on page unload
    window.addEventListener('beforeunload', function () {
        logout();
    });

    return {
        init: init,
        login: login,
        logout: logout,
        getOnlineUsers: getOnlineUsers,
        getOnlineCount: getOnlineCount,
        getCurrentUser: getCurrentUser,
        isLoggedIn: isLoggedIn,
        onUpdate: onUpdate
    };
})();
