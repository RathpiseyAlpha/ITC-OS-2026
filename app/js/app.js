// ─── Main Application Logic ───
// Boot sequence, matrix rain, explorer, views, router, login — all wired together.

(function () {
    'use strict';

    // ──────────────────────────────────────
    //  Utilities
    // ──────────────────────────────────────
    function escapeHtml(str) {
        var d = document.createElement('div');
        d.textContent = str;
        return d.innerHTML;
    }

    function getIcon(name, isDir) {
        if (isDir) return '📁';
        var ext = name.split('.').pop().toLowerCase();
        if (ext === 'pdf') return '📄';
        if (ext === 'md') return '📝';
        if (ext === 'html') return '🌐';
        if (['png', 'jpg', 'jpeg', 'gif', 'svg'].includes(ext)) return '🖼️';
        return '📄';
    }

    function getExt(name) {
        return name.split('.').pop().toLowerCase();
    }

    // ──────────────────────────────────────
    //  Matrix Rain Background
    // ──────────────────────────────────────
    var canvas = document.getElementById('matrix-bg');
    var ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    var chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01';
    var fontSize = 14;
    var columns = Math.floor(canvas.width / fontSize);
    var drops = Array(columns).fill(1);

    function drawMatrix() {
        ctx.fillStyle = 'rgba(10, 14, 20, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';

        for (var i = 0; i < drops.length; i++) {
            var text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(drawMatrix, 50);

    window.addEventListener('resize', function () {
        columns = Math.floor(canvas.width / fontSize);
        drops = Array(columns).fill(1);
    });

    // ──────────────────────────────────────
    //  Boot Sequence
    // ──────────────────────────────────────
    var bootLines = [
        { text: 'BIOS POST... OK', cls: 'boot-ok' },
        { text: 'Detecting hardware...', cls: 'boot-info' },
        { text: '  CPU: Multi-core processor detected', cls: 'boot-info' },
        { text: '  RAM: Memory check passed', cls: 'boot-ok' },
        { text: '  DISK: Storage device ready', cls: 'boot-ok' },
        { text: 'Loading kernel... vmlinuz-itc-os-2026', cls: 'boot-info' },
        { text: 'Mounting root filesystem...', cls: 'boot-info' },
        { text: 'Starting system services...', cls: 'boot-info' },
        { text: '  [  OK  ] Started course-materials.service', cls: 'boot-ok' },
        { text: '  [  OK  ] Started lecture-slides.service', cls: 'boot-ok' },
        { text: '  [  OK  ] Started lab-instructions.service', cls: 'boot-ok' },
        { text: '  [  OK  ] Started presence-tracking.service', cls: 'boot-ok' },
        { text: '', cls: 'boot-info' },
        { text: 'ITC Operating Systems 2026 — Ready.', cls: 'boot-ok' }
    ];

    var bootScreen = document.getElementById('boot-screen');
    var bootText = document.getElementById('boot-text');

    async function runBoot() {
        for (var i = 0; i < bootLines.length; i++) {
            var line = document.createElement('div');
            line.className = 'boot-line ' + bootLines[i].cls;
            line.textContent = bootLines[i].text;
            bootText.appendChild(line);
            await new Promise(function (r) { setTimeout(r, 120); });
            line.style.opacity = '1';
        }
        await new Promise(function (r) { setTimeout(r, 600); });
        bootScreen.classList.add('hidden');
        setTimeout(function () { bootScreen.style.display = 'none'; }, 800);
    }

    runBoot();

    // ──────────────────────────────────────
    //  Presence Init (dual-mode)
    // ──────────────────────────────────────
    Presence.init();

    // Web visitors (Firebase)
    Presence.onWebUpdate(function (users) {
        renderWebUsers(users);
        updateFooterPresence();
    });

    // Server users (Linux `who`)
    Presence.onServerUpdate(function (users) {
        renderServerUsers(users);
        updateFooterPresence();
    });

    function renderWebUsers(users) {
        var container = document.getElementById('web-users');
        if (!container) return;
        if (!users || users.length === 0) {
            container.innerHTML = '<li style="color:var(--comment);font-size:10px;padding:3px 8px;">No web visitors</li>';
        } else {
            var html = '';
            users.forEach(function (u) {
                html += '<li><span class="online-dot"></span>'
                    + '<span class="user-name' + (u.isSelf ? ' self' : '') + '">'
                    + escapeHtml(u.name) + (u.isSelf ? ' (you)' : '')
                    + '</span></li>';
            });
            container.innerHTML = html;
        }
        var countEl = document.getElementById('web-count');
        if (countEl) countEl.textContent = (users && users.length) ? users.length + ' online' : '';
    }

    function renderServerUsers(users) {
        var container = document.getElementById('server-users');
        if (!container) return;
        if (!users || users.length === 0) {
            container.innerHTML = '<li style="color:var(--comment);font-size:10px;padding:3px 8px;">No users logged in</li>';
        } else {
            var html = '';
            users.forEach(function (u) {
                var detail = u.terminal || '';
                if (u.host) detail += ' (' + escapeHtml(u.host) + ')';
                html += '<li title="' + escapeHtml(detail) + '">'
                    + '<span class="online-dot server"></span>'
                    + '<span class="user-name' + (u.isSelf ? ' self' : '') + '">'
                    + escapeHtml(u.name) + (u.isSelf ? ' (you)' : '')
                    + '</span>'
                    + (u.terminal ? '<span style="color:var(--comment);font-size:9px;margin-left:4px;">' + escapeHtml(u.terminal) + '</span>' : '')
                    + '</li>';
            });
            container.innerHTML = html;
        }
        var countEl = document.getElementById('server-count');
        if (countEl) countEl.textContent = (users && users.length) ? users.length + ' online' : '';
    }

    function updateFooterPresence() {
        var el = document.getElementById('footer-presence');
        if (!el) return;
        var wc = Presence.getWebCount();
        var sc = Presence.getServerCount();
        var parts = [];
        if (wc > 0) parts.push(wc + ' web');
        if (sc > 0) parts.push(sc + ' server');
        el.textContent = parts.length > 0 ? '\uD83D\uDC65 ' + parts.join(' \u2022 ') : '';
    }

    // ──────────────────────────────────────
    //  Sidebar Collapse / Section Toggles
    // ──────────────────────────────────────
    window.collapseSidebar = function () {
        var sidebar = document.getElementById('sidebar');
        var btn = document.getElementById('sidebar-collapse-btn');
        var contentsPage = document.getElementById('contents-page');
        sidebar.classList.toggle('collapsed');
        if (sidebar.classList.contains('collapsed')) {
            btn.innerHTML = '\u276F';
            btn.title = 'Expand sidebar';
            contentsPage.style.left = '36px';
        } else {
            btn.innerHTML = '\u276E';
            btn.title = 'Collapse sidebar';
            contentsPage.style.left = '220px';
        }
    };

    window.toggleSection = function (sectionId) {
        var list = document.getElementById(sectionId);
        var arrow = document.getElementById(sectionId + '-arrow');
        if (!list) return;
        var hidden = list.style.display === 'none';
        list.style.display = hidden ? '' : 'none';
        if (arrow) arrow.textContent = hidden ? '\u25BC' : '\u25B6';
    };

    // ──────────────────────────────────────
    //  Auth State
    // ──────────────────────────────────────
    var authToken = sessionStorage.getItem('authToken') || '';
    var authRole = sessionStorage.getItem('authRole') || '';
    var authUser = sessionStorage.getItem('authUser') || '';

    function serverUrl() {
        return (CONFIG.server && CONFIG.server.url) ? CONFIG.server.url.replace(/\/+$/, '') : '';
    }

    function setAuth(token, role, user) {
        authToken = token; authRole = role; authUser = user;
        sessionStorage.setItem('authToken', token);
        sessionStorage.setItem('authRole', role);
        sessionStorage.setItem('authUser', user);
        // Show admin nav link if admin
        var adminNav = document.getElementById('admin-nav');
        if (adminNav) adminNav.style.display = (role === 'admin') ? '' : 'none';
        // Show grades nav for authenticated students
        var gradesNav = document.getElementById('grades-nav');
        if (gradesNav) gradesNav.style.display = (role === 'user') ? '' : 'none';
    }

    function clearAuth() {
        authToken = ''; authRole = ''; authUser = '';
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('authRole');
        sessionStorage.removeItem('authUser');
        var adminNav = document.getElementById('admin-nav');
        if (adminNav) adminNav.style.display = 'none';
        var gradesNav = document.getElementById('grades-nav');
        if (gradesNav) gradesNav.style.display = 'none';
    }

    // Restore nav links on reload
    if (authRole === 'admin') {
        var adminNav = document.getElementById('admin-nav');
        if (adminNav) adminNav.style.display = '';
    }
    if (authRole === 'user') {
        var gradesNav = document.getElementById('grades-nav');
        if (gradesNav) gradesNav.style.display = '';
    }

    // ──────────────────────────────────────
    //  Session Restore on Refresh
    // ──────────────────────────────────────
    var restoringSession = false;
    (function restoreSession() {
        if (!authToken || !authUser) return;
        var url = serverUrl();
        if (!url) return;
        // Immediately hide login form while verifying
        restoringSession = true;
        var userLine = document.getElementById('username-line');
        var pwLine = document.getElementById('password-line');
        var guestArea = document.getElementById('guest-login-btn');
        if (userLine) userLine.style.display = 'none';
        if (pwLine) pwLine.style.display = 'none';
        if (guestArea && guestArea.parentElement) guestArea.parentElement.style.display = 'none';

        fetch(url + '/api/auth/verify', {
            method: 'POST',
            mode: 'cors',
            headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.valid) {
                finishLogin(authUser, true);
            } else {
                clearAuth();
                restoringSession = false;
                // Show login form again
                if (userLine) userLine.style.display = '';
                if (pwLine && serverUrl()) pwLine.style.display = '';
                if (guestArea && guestArea.parentElement) guestArea.parentElement.style.display = '';
            }
        })
        .catch(function () {
            restoringSession = false;
            // Server unreachable — show login form
            if (userLine) userLine.style.display = '';
            if (pwLine && serverUrl()) pwLine.style.display = '';
            if (guestArea && guestArea.parentElement) guestArea.parentElement.style.display = '';
        });
    })();

    // ──────────────────────────────────────
    //  Login System
    // ──────────────────────────────────────
    window.performLogin = function (username, password) {
        var name = username.trim();
        if (!name) return;

        var input = document.getElementById('login-input');
        var pwInput = document.getElementById('password-input');
        var output = document.getElementById('login-output');
        input.disabled = true;
        if (pwInput) pwInput.disabled = true;
        input.style.color = 'var(--white)';

        var pw = (password || (pwInput ? pwInput.value : '')).trim();
        var url = serverUrl();

        // If password provided and server URL available, do real auth
        if (pw && url) {
            output.innerHTML = '<div class="login-status">Authenticating against server...</div>';
            fetch(url + '/api/auth/login', {
                method: 'POST',
                mode: 'cors',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: name, password: pw })
            })
            .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, data: d }; }); })
            .then(function (res) {
                if (!res.ok) {
                    output.innerHTML = '<div class="error" style="margin-top:4px;">' + escapeHtml(res.data.error || 'Authentication failed.') + '</div>';
                    input.disabled = false;
                    if (pwInput) pwInput.disabled = false;
                    return;
                }
                setAuth(res.data.token, res.data.role, name);
                finishLogin(name, true);
            })
            .catch(function () {
                output.innerHTML = '<div class="error" style="margin-top:4px;">Server unreachable. Try guest login.</div>';
                input.disabled = false;
                if (pwInput) pwInput.disabled = false;
            });
        } else {
            // Guest login
            output.innerHTML = '<div class="login-status">Authenticating...</div>';
            setTimeout(function () {
                output.innerHTML = '<div class="login-status">Authenticating... done.</div>';
                setTimeout(function () { finishLogin(name, false); }, 500);
            }, 800);
        }
    };

    function finishLogin(name, authenticated) {
        var output = document.getElementById('login-output');
        // Register presence
        Presence.login(name);

        // Hide login input lines (important for session restore on refresh)
        var userLine = document.getElementById('username-line');
        var pwLine = document.getElementById('password-line');
        if (userLine) userLine.style.display = 'none';
        if (pwLine) pwLine.style.display = 'none';

        // Hide guest login area after any login
        var guestArea = document.getElementById('guest-login-btn');
        if (guestArea && guestArea.parentElement) guestArea.parentElement.style.display = 'none';

        // Update terminal prompt username
        var promptUsers = document.querySelectorAll('.prompt-user');
        promptUsers.forEach(function (el) { el.textContent = name; });

        var now = new Date();
        var ts = now.toLocaleDateString('en-US', { timeZone: 'Asia/Phnom_Penh', weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
            + ' ' + now.toLocaleTimeString('en-US', { timeZone: 'Asia/Phnom_Penh', hour: '2-digit', minute: '2-digit' });

        var badge = authenticated
            ? '<span style="color:var(--green);">&#x1F512; authenticated</span>'
            : '<span style="color:var(--comment);">guest</span>';

        var logoutBtn = ' <span id="logout-btn" style="color:var(--red);cursor:pointer;font-size:11px;border-bottom:1px dashed var(--red);margin-left:12px;" onclick="performLogout()">exit ↩</span>';

        output.innerHTML = '<div class="login-success">\u2714 Login successful. ' + badge + logoutBtn + '</div>'
            + '<div class="login-motd">'
            + 'Welcome to ITC-OS 2026, <span style="color:var(--cyan)">' + escapeHtml(name) + '</span>!<br>'
            + 'Last login: ' + ts + ' on tty1<br>'
            + 'Type <span style="color:var(--white)">help</span> for available commands.'
            + '</div>';

        // Enable enter prompt
        var ep = document.getElementById('enter-prompt');
        ep.style.pointerEvents = 'auto';
        ep.style.opacity = '1';
        ep.innerHTML = '<span class="prompt-symbol">$</span> Press <span style="color:var(--green)">Enter</span> or click here to explore the system <span class="cursor"></span>';
        ep.onclick = enterExplorer;
    }

    window.guestLogin = function () {
        window.performLogin('guest', '');
    };

    window.performLogout = function () {
        var url = serverUrl();
        if (url && authToken) {
            fetch(url + '/api/auth/logout', {
                method: 'POST',
                mode: 'cors',
                headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken }
            }).catch(function () {});
        }
        clearAuth();
        Presence.logout();
        // Reset login UI
        var input = document.getElementById('login-input');
        var pwInput = document.getElementById('password-input');
        var output = document.getElementById('login-output');
        var ep = document.getElementById('enter-prompt');
        if (input) { input.disabled = false; input.value = ''; input.style.color = ''; }
        if (pwInput) { pwInput.disabled = false; pwInput.value = ''; }
        if (output) output.innerHTML = '';
        // Restore login input lines
        var userLine = document.getElementById('username-line');
        var pwLine = document.getElementById('password-line');
        if (userLine) userLine.style.display = '';
        if (pwLine) pwLine.style.display = serverUrl() ? '' : 'none';
        if (ep) { ep.style.pointerEvents = 'none'; ep.style.opacity = '0.3'; ep.innerHTML = '<span class="prompt-symbol">$</span> Login to explore the system <span class="cursor"></span>'; ep.onclick = null; }
        // Restore guest login area
        var guestArea = document.getElementById('guest-login-btn');
        if (guestArea && guestArea.parentElement) guestArea.parentElement.style.display = '';
        // Go back to landing
        document.getElementById('contents-page').classList.remove('active');
        document.getElementById('landing-page').classList.remove('hidden');
        window.location.hash = '';
        if (input) setTimeout(function () { input.focus(); }, 200);
    };

    // Login input handler
    (function () {
        var loginInput = document.getElementById('login-input');
        var pwInput = document.getElementById('password-input');
        var pwLine = document.getElementById('password-line');
        var hasServer = !!serverUrl();

        // When server is configured, show password field (but not during session restore)
        if (hasServer && pwLine && !restoringSession) {
            pwLine.style.display = '';
        }

        if (loginInput) {
            loginInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    e.stopPropagation();
                    if (hasServer && pwInput && !pwInput.value.trim()) {
                        pwInput.focus();
                        return;
                    }
                    window.performLogin(loginInput.value);
                }
            });
            setTimeout(function () { loginInput.focus(); }, 3500);
        }

        if (pwInput) {
            pwInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    e.stopPropagation();
                    window.performLogin(loginInput.value);
                }
            });
        }
    })();

    // ──────────────────────────────────────
    //  Admin Panel (Tabbed: Stats | Grades | Leaderboard)
    // ──────────────────────────────────────
    var adminCurrentTab = 'stats';

    function renderAdminPanel(tab) {
        if (authRole !== 'admin') {
            window.location.hash = 'browse';
            return;
        }
        var url = serverUrl();
        if (!url) return;
        adminCurrentTab = tab || adminCurrentTab || 'stats';

        var viewerEl = document.getElementById('file-viewer');
        var outlineEl = document.getElementById('outline-content');
        outlineEl.style.display = 'none';
        document.getElementById('viewer-placeholder').style.display = 'none';
        document.getElementById('viewer-title').textContent = 'bash — admin';

        viewerEl.style.display = 'flex';

        // Also update explorer pane title
        document.getElementById('explorer-title').textContent = 'bash — admin';
        document.getElementById('explorer-cmd').textContent = 'sudo admin --' + adminCurrentTab;

        var tabsHtml = '<div class="admin-tabs">'
            + '<span class="admin-tab' + (adminCurrentTab === 'stats' ? ' active' : '') + '" onclick="switchAdminTab(\'stats\')">Users</span>'
            + '<span class="admin-tab' + (adminCurrentTab === 'grades' ? ' active' : '') + '" onclick="switchAdminTab(\'grades\')">Grades</span>'
            + '<span class="admin-tab' + (adminCurrentTab === 'leaderboard' ? ' active' : '') + '" onclick="switchAdminTab(\'leaderboard\')">Leaderboard</span>'
            + '</div>';

        viewerEl.innerHTML = '<div class="admin-panel">' + tabsHtml + '<div id="admin-tab-content"><div class="admin-loading">Loading...</div></div></div>';

        if (adminCurrentTab === 'stats') fetchAdminStats(url);
        else if (adminCurrentTab === 'grades') fetchAdminGrades(url);
        else if (adminCurrentTab === 'leaderboard') fetchAdminLeaderboard(url);
    }

    window.switchAdminTab = function (tab) {
        adminCurrentTab = tab;
        renderAdminPanel(tab);
    };

    function adminContent() {
        return document.getElementById('admin-tab-content');
    }

    // ── Admin Search Helper ──
    function adminSearchHtml(id, placeholder) {
        return '<div class="admin-search-bar">'
            + '<input type="text" id="' + id + '" placeholder="' + placeholder + '" oninput="adminFilterTable(\'' + id + '\')">'
            + '<span class="admin-search-count" id="' + id + '-count"></span>'
            + '</div>';
    }

    window.adminFilterTable = function (inputId) {
        var input = document.getElementById(inputId);
        if (!input) return;
        var query = input.value.toLowerCase();
        var container = input.closest('.admin-panel') || adminContent();
        var table = container.querySelector('.admin-table');
        if (!table) return;
        var rows = table.querySelectorAll('tbody tr');
        var visible = 0;
        for (var i = 0; i < rows.length; i++) {
            var text = rows[i].textContent.toLowerCase();
            var show = !query || text.indexOf(query) !== -1;
            rows[i].style.display = show ? '' : 'none';
            if (show) visible++;
        }
        var countEl = document.getElementById(inputId + '-count');
        if (countEl) {
            countEl.textContent = query ? visible + ' / ' + rows.length : '';
        }
    };

    // ── Admin Table Sort ──
    var _adminSortCol = -1;
    var _adminSortAsc = true;

    window.adminSortTable = function (th) {
        var table = th.closest('table');
        if (!table) return;
        var headers = th.parentNode.querySelectorAll('th');
        var colIdx = Array.prototype.indexOf.call(headers, th);
        if (colIdx === _adminSortCol) {
            _adminSortAsc = !_adminSortAsc;
        } else {
            _adminSortCol = colIdx;
            _adminSortAsc = true;
        }
        // Update sort indicators
        for (var h = 0; h < headers.length; h++) {
            headers[h].classList.remove('sort-asc', 'sort-desc');
        }
        th.classList.add(_adminSortAsc ? 'sort-asc' : 'sort-desc');

        var tbody = table.querySelector('tbody');
        var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
        rows.sort(function (a, b) {
            var aText = (a.children[colIdx] || {}).textContent || '';
            var bText = (b.children[colIdx] || {}).textContent || '';
            // Try numeric comparison first
            var aNum = parseFloat(aText.replace(/[^0-9.\-]/g, ''));
            var bNum = parseFloat(bText.replace(/[^0-9.\-]/g, ''));
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return _adminSortAsc ? aNum - bNum : bNum - aNum;
            }
            // Fall back to string comparison
            var cmp = aText.localeCompare(bText, undefined, { numeric: true, sensitivity: 'base' });
            return _adminSortAsc ? cmp : -cmp;
        });
        for (var i = 0; i < rows.length; i++) {
            tbody.appendChild(rows[i]);
        }
    };

    // ── Stats Tab ──
    function fetchAdminStats(url) {
        var container = adminContent();
        if (!container) return;
        container.innerHTML = '<div class="admin-loading">Fetching stats...</div>';
        fetch(url + '/api/admin/stats', {
            mode: 'cors',
            headers: { 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(function (data) {
            var users = data.users || [];
            var html = '<div class="admin-section-header">User Activity Statistics'
                + ' <span id="admin-refresh-btn" style="color:var(--cyan);cursor:pointer;font-size:11px;border-bottom:1px dashed var(--cyan);margin-left:12px;" onclick="refreshAdminStats()">&#x21BB; refresh</span>'
                + '</div>'
                + '<div class="admin-summary">'
                + '<span class="admin-stat"><span class="admin-stat-val">' + users.length + '</span> total users</span>'
                + '<span class="admin-stat"><span class="admin-stat-val">' + users.filter(function(u){return u.isOnline;}).length + '</span> online now</span>'
                + '</div>'
                + adminSearchHtml('admin-search-users', '\uD83D\uDD0D Search users...')
                + '<table class="admin-table">'
                + '<thead><tr><th onclick="adminSortTable(this)">User</th><th onclick="adminSortTable(this)">Logins</th><th onclick="adminSortTable(this)">Last Login</th><th onclick="adminSortTable(this)">Duration</th><th onclick="adminSortTable(this)">Status</th></tr></thead>'
                + '<tbody>';

            if (users.length === 0) {
                html += '<tr><td colspan="5" style="color:var(--comment);text-align:center;">No users found</td></tr>';
            } else {
                users.forEach(function (u) {
                    var status = u.isOnline
                        ? '<span class="admin-online">\u25CF online</span>'
                        : '<span class="admin-offline">\u25CB offline</span>';
                    var lastLogin = u.lastLogin ? formatPhnomPenh(u.lastLogin) : '\u2014';
                    html += '<tr>'
                        + '<td class="admin-user">' + escapeHtml(u.username) + '</td>'
                        + '<td>' + u.loginCount + '</td>'
                        + '<td>' + escapeHtml(lastLogin) + '</td>'
                        + '<td>' + escapeHtml(u.totalDuration || '0h 0m') + '</td>'
                        + '<td>' + status + '</td>'
                        + '</tr>';
                });
            }

            html += '</tbody></table>';
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load stats: ' + escapeHtml(err.message) + '</div>';
        });
    }

    window.refreshAdminStats = function () {
        var url = serverUrl();
        if (!url) return;
        var btn = document.getElementById('admin-refresh-btn');
        if (btn) btn.textContent = '\u21BB loading...';
        fetchAdminStats(url);
    };

    // ── Grades Tab ──
    var gradesLabFilter = null;

    function fetchAdminGrades(url, labFilter) {
        var container = adminContent();
        if (!container) return;
        gradesLabFilter = labFilter || null;
        container.innerHTML = '<div class="admin-loading">Grading submissions...</div>';

        var endpoint = url + '/api/admin/grades';
        if (gradesLabFilter) endpoint += '?lab=' + encodeURIComponent(gradesLabFilter);

        fetch(endpoint, {
            mode: 'cors',
            headers: { 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(function (data) {
            var grades = data.grades || [];
            var labs = data.labs || [];

            // Lab filter buttons
            var html = '<div class="admin-section-header">Lab Grading'
                + ' <span style="color:var(--cyan);cursor:pointer;font-size:11px;border-bottom:1px dashed var(--cyan);margin-left:12px;" onclick="fetchAdminGrades_refresh()">&#x21BB; refresh</span>'
                + '</div>'
                + '<div class="admin-lab-filters">'
                + '<span class="admin-lab-btn' + (!gradesLabFilter ? ' active' : '') + '" onclick="filterGrades(null)">All Labs</span>';
            labs.forEach(function (l) {
                html += '<span class="admin-lab-btn' + (gradesLabFilter === l ? ' active' : '') + '" onclick="filterGrades(\'' + l + '\')">' + escapeHtml(l) + '</span>';
            });
            html += '</div>';

            if (grades.length === 0) {
                html += '<div style="color:var(--comment);padding:12px;">No submissions found.</div>';
            } else {
                html += adminSearchHtml('admin-search-grades', '\uD83D\uDD0D Search by ID, name, score...')
                    + '<table class="admin-table">'
                    + '<thead><tr><th onclick="adminSortTable(this)">ID</th><th onclick="adminSortTable(this)">Name</th><th onclick="adminSortTable(this)">Lab</th><th onclick="adminSortTable(this)">Score</th><th onclick="adminSortTable(this)">%</th><th onclick="adminSortTable(this)">Status</th><th>Details</th></tr></thead>'
                    + '<tbody>';
                grades.forEach(function (g) {
                    var pctClass = g.percentage >= 80 ? 'grade-a' : g.percentage >= 50 ? 'grade-b' : 'grade-c';
                    var statusIcon = g.found ? (g.percentage === 100 ? '\u2705' : '\u26A0\uFE0F') : '\u274C';
                    html += '<tr>'
                        + '<td class="admin-user">' + escapeHtml(g.id || g.username) + '</td>'
                        + '<td>' + escapeHtml(g.name || g.username) + '</td>'
                        + '<td>' + escapeHtml(g.lab) + '</td>'
                        + '<td><span class="' + pctClass + '">' + g.score + '/' + g.total + '</span></td>'
                        + '<td><span class="' + pctClass + '">' + g.percentage + '%</span></td>'
                        + '<td>' + statusIcon + '</td>'
                        + '<td><span class="admin-detail-btn" onclick="showGradeDetail(\'' + escapeHtml(g.username) + '\',\'' + escapeHtml(g.lab) + '\')">view</span></td>'
                        + '</tr>';
                });
                html += '</tbody></table>';
            }
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load grades: ' + escapeHtml(err.message) + '</div>';
        });
    }

    window.filterGrades = function (lab) {
        var url = serverUrl();
        if (url) fetchAdminGrades(url, lab);
    };

    window.fetchAdminGrades_refresh = function () {
        var url = serverUrl();
        if (url) fetchAdminGrades(url, gradesLabFilter);
    };

    window.showGradeDetail = function (username, lab) {
        var url = serverUrl();
        if (!url) return;
        var container = adminContent();
        if (!container) return;
        container.innerHTML = '<div class="admin-loading">Loading details for ' + escapeHtml(username) + ' / ' + escapeHtml(lab) + '...</div>';

        // Fetch grade detail and file tree in parallel
        Promise.all([
            fetch(url + '/api/admin/grades?user=' + encodeURIComponent(username) + '&lab=' + encodeURIComponent(lab), {
                mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
            }).then(function (r) { return r.json(); }),
            fetch(url + '/api/admin/tree?user=' + encodeURIComponent(username) + '&lab=' + encodeURIComponent(lab), {
                mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
            }).then(function (r) { return r.ok ? r.json() : null; })
        ])
        .then(function (results) {
            var g = results[0];
            var tree = results[1];

            var html = '<div class="admin-section-header">'
                + '<span class="admin-back-btn" onclick="switchAdminTab(\'grades\')">\u2190 back</span> '
                + escapeHtml(username) + ' / ' + escapeHtml(lab)
                + ' \u2014 <span class="' + (g.percentage >= 80 ? 'grade-a' : g.percentage >= 50 ? 'grade-b' : 'grade-c') + '">'
                + g.score + '/' + g.total + ' (' + g.percentage + '%)</span>'
                + '</div>';

            if (g.labPath) {
                html += '<div style="color:var(--comment);font-size:11px;margin-bottom:8px;">' + escapeHtml(g.labPath) + '</div>';
            }

            // File tree
            if (tree && tree.tree) {
                html += '<div class="grade-detail-columns"><div class="grade-tree-col">'
                    + '<div style="color:var(--cyan);font-size:12px;margin-bottom:4px;">File Tree:</div>'
                    + '<pre class="grade-tree">' + renderTreeText(tree.tree, '') + '</pre>'
                    + '</div>';
            }

            // Items checklist
            html += '<div class="grade-items-col">'
                + '<div style="color:var(--cyan);font-size:12px;margin-bottom:4px;">Checklist:</div>'
                + '<div class="grade-items">';
            (g.items || []).forEach(function (item) {
                var icon = item.status === 'ok' ? '\u2705' : item.status === 'case_mismatch' ? '\u26A0\uFE0F' : '\u274C';
                var cls = item.status === 'ok' ? 'item-ok' : item.status === 'case_mismatch' ? 'item-warn' : 'item-miss';
                var detail = '';
                if (item.status === 'case_mismatch') detail = ' (found as: ' + escapeHtml(item.actual) + ')';
                html += '<div class="grade-item ' + cls + '">'
                    + icon + ' <span class="grade-item-name">' + escapeHtml(item.expected) + '</span>'
                    + ' <span class="grade-item-pts">' + item.points + '/' + item.maxPoints + '</span>'
                    + detail
                    + '</div>';
            });
            html += '</div></div>';

            if (tree && tree.tree) html += '</div>'; // close columns

            // Feedback
            if (g.feedback && g.feedback.length > 0) {
                html += '<div style="margin-top:12px;"><div style="color:var(--red);font-size:12px;margin-bottom:4px;">Feedback:</div>';
                g.feedback.forEach(function (f) {
                    html += '<div class="grade-feedback">\u2022 ' + escapeHtml(f) + '</div>';
                });
                html += '</div>';
            }
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed: ' + escapeHtml(err.message) + '</div>';
        });
    };

    function renderTreeText(nodes, prefix) {
        var lines = '';
        for (var i = 0; i < nodes.length; i++) {
            var node = nodes[i];
            var isLast = i === nodes.length - 1;
            var connector = isLast ? '\u2514\u2500\u2500 ' : '\u251C\u2500\u2500 ';
            var icon = node.type === 'dir' ? '\uD83D\uDCC1 ' : '';
            lines += prefix + connector + icon + escapeHtml(node.name) + '\n';
            if (node.children && node.children.length > 0) {
                var childPrefix = prefix + (isLast ? '    ' : '\u2502   ');
                lines += renderTreeText(node.children, childPrefix);
            }
        }
        return lines;
    }

    // ── Leaderboard Tab ──
    function fetchAdminLeaderboard(url) {
        var container = adminContent();
        if (!container) return;
        container.innerHTML = '<div class="admin-loading">Computing leaderboard...</div>';

        fetch(url + '/api/admin/leaderboard', {
            mode: 'cors',
            headers: { 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return r.json();
        })
        .then(function (data) {
            var board = data.leaderboard || [];
            var labs = data.labs || [];

            var html = '<div class="admin-section-header">Student Leaderboard'
                + ' <span style="color:var(--cyan);cursor:pointer;font-size:11px;border-bottom:1px dashed var(--cyan);margin-left:12px;" onclick="switchAdminTab(\'leaderboard\')">&#x21BB; refresh</span>'
                + '</div>';

            html += adminSearchHtml('admin-search-leaderboard', '\uD83D\uDD0D Search students...')
                + '<table class="admin-table leaderboard-table">'
                + '<thead><tr><th onclick="adminSortTable(this)">#</th><th onclick="adminSortTable(this)">ID</th><th onclick="adminSortTable(this)">Name</th>';
            labs.forEach(function (l) { html += '<th onclick="adminSortTable(this)">' + escapeHtml(l) + '</th>'; });
            html += '<th onclick="adminSortTable(this)">Total</th><th onclick="adminSortTable(this)">%</th></tr></thead><tbody>';

            if (board.length === 0) {
                html += '<tr><td colspan="' + (labs.length + 5) + '" style="color:var(--comment);text-align:center;">No students found</td></tr>';
            } else {
                board.forEach(function (s) {
                    var rankIcon = s.rank === 1 ? '\uD83E\uDD47' : s.rank === 2 ? '\uD83E\uDD48' : s.rank === 3 ? '\uD83E\uDD49' : s.rank;
                    var pctClass = s.totalPercentage >= 80 ? 'grade-a' : s.totalPercentage >= 50 ? 'grade-b' : 'grade-c';
                    html += '<tr>'
                        + '<td class="rank-cell">' + rankIcon + '</td>'
                        + '<td class="admin-user">' + escapeHtml(s.id || s.username) + '</td>'
                        + '<td>' + escapeHtml(s.name || s.username) + '</td>';
                    labs.forEach(function (l) {
                        var labData = s.labs[l];
                        if (labData) {
                            var lc = labData.percentage >= 80 ? 'grade-a' : labData.percentage >= 50 ? 'grade-b' : 'grade-c';
                            html += '<td><span class="' + lc + '">' + labData.score + '/' + labData.total + '</span></td>';
                        } else {
                            html += '<td style="color:var(--comment);">\u2014</td>';
                        }
                    });
                    html += '<td><span class="' + pctClass + '">' + s.totalScore + '/' + s.totalPossible + '</span></td>'
                        + '<td><span class="' + pctClass + '">' + s.totalPercentage + '%</span></td>'
                        + '</tr>';
                });
            }

            html += '</tbody></table>';
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load leaderboard: ' + escapeHtml(err.message) + '</div>';
        });
    }

    // ──────────────────────────────────────
    //  Student Grades Panel (Tabbed: My Grades | Leaderboard)
    // ──────────────────────────────────────
    var studentCurrentTab = 'my-grades';

    function renderStudentGrades(tab) {
        if (!authToken || authRole === 'admin') {
            window.location.hash = 'browse';
            return;
        }
        var url = serverUrl();
        if (!url) return;
        studentCurrentTab = tab || studentCurrentTab || 'my-grades';

        var viewerEl = document.getElementById('file-viewer');
        var outlineEl = document.getElementById('outline-content');
        outlineEl.style.display = 'none';
        document.getElementById('viewer-placeholder').style.display = 'none';
        document.getElementById('viewer-title').textContent = 'bash — grades';

        viewerEl.style.display = 'flex';
        document.getElementById('explorer-title').textContent = 'bash — grades';
        document.getElementById('explorer-cmd').textContent = 'cat grades/' + studentCurrentTab;

        var tabsHtml = '<div class="admin-tabs">'
            + '<span class="admin-tab' + (studentCurrentTab === 'my-grades' ? ' active' : '') + '" onclick="switchStudentTab(\'my-grades\')">My Grades</span>'
            + '<span class="admin-tab' + (studentCurrentTab === 'leaderboard' ? ' active' : '') + '" onclick="switchStudentTab(\'leaderboard\')">Leaderboard</span>'
            + '</div>';

        viewerEl.innerHTML = '<div class="admin-panel">' + tabsHtml + '<div id="student-tab-content"><div class="admin-loading">Loading...</div></div></div>';

        if (studentCurrentTab === 'my-grades') fetchStudentGrades(url);
        else if (studentCurrentTab === 'leaderboard') fetchStudentLeaderboard(url);
    }

    window.switchStudentTab = function (tab) {
        studentCurrentTab = tab;
        renderStudentGrades(tab);
    };

    function studentContent() {
        return document.getElementById('student-tab-content');
    }

    // ── My Grades Tab ──
    function fetchStudentGrades(url) {
        var container = studentContent();
        if (!container) return;
        fetch(url + '/api/my/grades', {
            mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.error) {
                container.innerHTML = '<div class="error" style="padding:12px;">' + escapeHtml(data.error) + '</div>';
                return;
            }
            var grades = data.grades || [];

            // Summary bar
            var totalScore = 0, totalPossible = 0;
            grades.forEach(function (g) { totalScore += g.score; totalPossible += g.total; });
            var totalPct = totalPossible > 0 ? Math.round(totalScore / totalPossible * 1000) / 10 : 0;
            var summaryClass = totalPct >= 80 ? 'grade-a' : totalPct >= 50 ? 'grade-b' : 'grade-c';

            var html = '<div class="student-summary">'
                + '<span class="student-summary-label">Overall:</span> '
                + '<span class="' + summaryClass + '">' + totalScore + '/' + totalPossible + ' (' + totalPct + '%)</span>'
                + '</div>';

            grades.forEach(function (g) {
                var pctClass = g.percentage >= 80 ? 'grade-a' : g.percentage >= 50 ? 'grade-b' : 'grade-c';
                var statusIcon = g.found ? (g.percentage === 100 ? '\u2705' : '\u26A0\uFE0F') : '\u274C';
                html += '<div class="student-lab-card">'
                    + '<div class="student-lab-header">'
                    + '<span class="student-lab-name">' + escapeHtml(g.lab) + '</span> '
                    + statusIcon + ' '
                    + '<span class="' + pctClass + '">' + g.score + '/' + g.total + ' (' + g.percentage + '%)</span>'
                    + ' <span class="admin-detail-btn" onclick="showStudentLabDetail(\'' + escapeHtml(g.lab) + '\')">view details</span>'
                    + '</div>';

                // Brief checklist summary
                if (g.items && g.items.length > 0) {
                    var okCount = 0, warnCount = 0, missCount = 0;
                    g.items.forEach(function (item) {
                        if (item.status === 'ok') okCount++;
                        else if (item.status === 'case_mismatch') warnCount++;
                        else missCount++;
                    });
                    html += '<div class="student-checklist-summary">'
                        + '\u2705 ' + okCount + ' ok';
                    if (warnCount > 0) html += ' &nbsp;\u26A0\uFE0F ' + warnCount + ' naming';
                    if (missCount > 0) html += ' &nbsp;\u274C ' + missCount + ' missing';
                    html += '</div>';
                }

                // Feedback
                if (g.feedback && g.feedback.length > 0) {
                    html += '<div class="grade-feedback">';
                    g.feedback.forEach(function (f) {
                        html += '<div>\u25B8 ' + escapeHtml(f) + '</div>';
                    });
                    html += '</div>';
                }
                html += '</div>';
            });
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load grades: ' + escapeHtml(err.message) + '</div>';
        });
    }

    // ── Student Leaderboard Tab ──
    function fetchStudentLeaderboard(url) {
        var container = studentContent();
        if (!container) return;
        fetch(url + '/api/my/leaderboard', {
            mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.error) {
                container.innerHTML = '<div class="error" style="padding:12px;">' + escapeHtml(data.error) + '</div>';
                return;
            }
            var board = data.leaderboard || [];
            var labs = data.labs || [];

            var html = '<table class="admin-table leaderboard-table">'
                + '<thead><tr><th onclick="adminSortTable(this)">#</th><th onclick="adminSortTable(this)">Name</th>';
            labs.forEach(function (l) { html += '<th onclick="adminSortTable(this)">' + escapeHtml(l) + '</th>'; });
            html += '<th onclick="adminSortTable(this)">Total</th><th onclick="adminSortTable(this)">%</th></tr></thead><tbody>';

            if (board.length === 0) {
                html += '<tr><td colspan="' + (labs.length + 4) + '" style="color:var(--comment);text-align:center;">No students found</td></tr>';
            } else {
                board.forEach(function (s) {
                    var rankIcon = s.rank === 1 ? '\uD83E\uDD47' : s.rank === 2 ? '\uD83E\uDD48' : s.rank === 3 ? '\uD83E\uDD49' : s.rank;
                    var pctClass = s.totalPercentage >= 80 ? 'grade-a' : s.totalPercentage >= 50 ? 'grade-b' : 'grade-c';
                    var isMe = s.username === authUser;
                    html += '<tr' + (isMe ? ' class="leaderboard-me"' : '') + '>'
                        + '<td class="rank-cell">' + rankIcon + '</td>'
                        + '<td>' + escapeHtml(s.name || s.username) + (isMe ? ' \u2B50' : '') + '</td>';
                    labs.forEach(function (l) {
                        var labData = s.labs[l];
                        if (labData) {
                            var lc = labData.percentage >= 80 ? 'grade-a' : labData.percentage >= 50 ? 'grade-b' : 'grade-c';
                            html += '<td><span class="' + lc + '">' + labData.score + '/' + labData.total + '</span></td>';
                        } else {
                            html += '<td style="color:var(--comment);">\u2014</td>';
                        }
                    });
                    html += '<td><span class="' + pctClass + '">' + s.totalScore + '/' + s.totalPossible + '</span></td>'
                        + '<td><span class="' + pctClass + '">' + s.totalPercentage + '%</span></td>'
                        + '</tr>';
                });
            }

            html += '</tbody></table>';
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load leaderboard: ' + escapeHtml(err.message) + '</div>';
        });
    }

    // ── Student Lab Detail View (tree + checklist) ──
    window.showStudentLabDetail = function (lab) {
        var url = serverUrl();
        if (!url || !authToken) return;
        var container = studentContent();
        if (!container) return;
        container.innerHTML = '<div class="admin-loading">Loading details for ' + escapeHtml(lab) + '...</div>';

        Promise.all([
            fetch(url + '/api/my/grades', {
                mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
            }).then(function (r) { return r.json(); }),
            fetch(url + '/api/my/tree?lab=' + encodeURIComponent(lab), {
                mode: 'cors', headers: { 'Authorization': 'Bearer ' + authToken }
            }).then(function (r) { return r.ok ? r.json() : null; })
        ])
        .then(function (results) {
            var data = results[0];
            var tree = results[1];

            // Find grade for this specific lab
            var g = null;
            (data.grades || []).forEach(function (gr) { if (gr.lab === lab) g = gr; });
            if (!g) {
                container.innerHTML = '<div class="error" style="padding:12px;">Grade data not found for ' + escapeHtml(lab) + '</div>';
                return;
            }

            var pctClass = g.percentage >= 80 ? 'grade-a' : g.percentage >= 50 ? 'grade-b' : 'grade-c';

            var html = '<div class="admin-section-header">'
                + '<span class="admin-back-btn" onclick="switchStudentTab(\'my-grades\')">\u2190 back</span> '
                + escapeHtml(lab)
                + ' \u2014 <span class="' + pctClass + '">'
                + g.score + '/' + g.total + ' (' + g.percentage + '%)</span>'
                + '</div>';

            if (g.labPath) {
                html += '<div style="color:var(--comment);font-size:11px;margin-bottom:8px;">' + escapeHtml(g.labPath) + '</div>';
            }

            // Two-column layout: tree + checklist
            html += '<div class="grade-detail-columns">';

            // File tree column
            if (tree && tree.tree) {
                html += '<div class="grade-tree-col">'
                    + '<div style="color:var(--cyan);font-size:12px;margin-bottom:4px;">Your File Tree:</div>'
                    + '<pre class="grade-tree">' + renderTreeText(tree.tree, '') + '</pre>'
                    + '</div>';
            } else {
                html += '<div class="grade-tree-col">'
                    + '<div style="color:var(--cyan);font-size:12px;margin-bottom:4px;">File Tree:</div>'
                    + '<div style="color:var(--comment);padding:8px;">Lab directory not found.</div>'
                    + '</div>';
            }

            // Checklist column
            html += '<div class="grade-items-col">'
                + '<div style="color:var(--cyan);font-size:12px;margin-bottom:4px;">Required Items:</div>'
                + '<div class="grade-items">';
            (g.items || []).forEach(function (item) {
                var icon = item.status === 'ok' ? '\u2705' : item.status === 'case_mismatch' ? '\u26A0\uFE0F' : '\u274C';
                var cls = item.status === 'ok' ? 'item-ok' : item.status === 'case_mismatch' ? 'item-warn' : 'item-miss';
                var detail = '';
                if (item.status === 'case_mismatch') detail = ' (found as: ' + escapeHtml(item.actual) + ')';
                html += '<div class="grade-item ' + cls + '">'
                    + icon + ' <span class="grade-item-name">' + escapeHtml(item.expected) + '</span>'
                    + ' <span class="grade-item-pts">' + item.points + '/' + item.maxPoints + '</span>'
                    + detail
                    + '</div>';
            });
            html += '</div></div></div>'; // close items, items-col, columns

            // Feedback section
            if (g.feedback && g.feedback.length > 0) {
                html += '<div style="margin-top:12px;"><div style="color:var(--red);font-size:12px;margin-bottom:4px;">Feedback:</div>';
                g.feedback.forEach(function (f) {
                    html += '<div class="grade-feedback">\u2022 ' + escapeHtml(f) + '</div>';
                });
                html += '</div>';
            }
            container.innerHTML = html;
        })
        .catch(function (err) {
            container.innerHTML = '<div class="error" style="padding:12px;">Failed to load details: ' + escapeHtml(err.message) + '</div>';
        });
    };

    function formatPhnomPenh(isoOrDateStr) {
        try {
            var d = new Date(isoOrDateStr);
            if (isNaN(d.getTime())) return isoOrDateStr;
            return d.toLocaleString('en-US', {
                timeZone: 'Asia/Phnom_Penh',
                year: 'numeric', month: 'short', day: 'numeric',
                hour: '2-digit', minute: '2-digit', hour12: true
            });
        } catch (e) { return isoOrDateStr; }
    }

    // ──────────────────────────────────────
    //  Explorer — Dynamic File Tree
    // ──────────────────────────────────────
    var explorerReady = false;

    window.navigateTo = function (path) {
        window.location.hash = path ? 'browse/' + path : 'browse';
    };

    window.viewFile = function (dirPath, fileName) {
        var filePath = dirPath ? dirPath + '/' + fileName : fileName;
        window.location.hash = 'view/' + filePath;
    };

    async function renderExplorer(path) {
        var tree = await GitHubAPI.getTree();
        var node = tree[path];

        if (!node) {
            // Path not found — go to root
            node = tree[''];
            path = '';
        }

        var parts = path ? path.split('/') : [];
        var listEl = document.getElementById('file-list');
        var viewerEl = document.getElementById('file-viewer');
        var breadEl = document.getElementById('explorer-breadcrumb');
        var cmdEl = document.getElementById('explorer-cmd');
        var titleEl = document.getElementById('explorer-title');

        viewerEl.style.display = 'none';
        viewerEl.innerHTML = '';

        // Breadcrumb
        var bc = '<a onclick="navigateTo(\'\')" style="cursor:pointer">~</a>';
        var cumulative = '';
        parts.forEach(function (p, i) {
            cumulative += (i > 0 ? '/' : '') + p;
            var cp = cumulative;
            bc += '<span class="sep">/</span>';
            if (i === parts.length - 1) {
                bc += '<span class="current-dir">' + escapeHtml(p) + '</span>';
            } else {
                bc += '<a onclick="navigateTo(\'' + cp + '\')" style="cursor:pointer">' + escapeHtml(p) + '</a>';
            }
        });
        bc += '<span class="sep">/</span>';
        breadEl.innerHTML = bc;
        cmdEl.textContent = 'ls -la ' + (path || '.');
        titleEl.textContent = 'bash — ' + (path || '~');

        // File listing
        var html = '';

        // Parent directory
        if (path) {
            var parent = parts.slice(0, -1).join('/');
            html += '<li onclick="navigateTo(\'' + parent + '\')"><span class="icon">⬆️</span><span class="fname dir">..</span><span class="fmeta">parent directory</span></li>';
        }

        // Directories
        node.dirs.forEach(function (d) {
            var fullPath = path ? path + '/' + d : d;
            var info = GitHubAPI.getNodeInfo(fullPath);
            var count = info ? info.total : 0;
            html += '<li onclick="navigateTo(\'' + fullPath + '\')"><span class="icon">📁</span><span class="fname dir">' + escapeHtml(d) + '/</span><span class="fmeta">' + count + ' items</span></li>';
        });

        // Files
        node.files.forEach(function (f) {
            html += '<li onclick="viewFile(\'' + path + '\',\'' + f.name + '\')"><span class="icon">' + getIcon(f.name) + '</span><span class="fname">' + escapeHtml(f.name) + '</span><span class="fmeta"></span></li>';
        });

        if (!node.dirs.length && !node.files.length) {
            if (path) {
                html += '<li onclick="navigateTo(\'' + parts.slice(0, -1).join('/') + '\')"><span class="icon">⬆️</span><span class="fname dir">..</span><span class="fmeta">parent directory</span></li>';
            }
            html += '<li><span class="fmeta" style="color:var(--yellow)">// empty — content coming soon</span></li>';
        }

        listEl.innerHTML = html;

        // Build sidebar dynamically
        await buildSidebar(tree);
    }

    // ──────────────────────────────────────
    //  Dynamic Sidebar
    // ──────────────────────────────────────
    async function buildSidebar(tree) {
        var scheduleEl = document.getElementById('sidebar-schedule');
        var progressEl = document.getElementById('sidebar-progress');
        if (!scheduleEl || !progressEl) return;

        // Schedule: check which lecture files actually exist
        var scheduleHtml = '';
        var availableCount = 0;
        CONFIG.schedule.forEach(function (item) {
            var exists = GitHubAPI.fileExists(item.file);
            if (exists) availableCount++;

            var weekStr = String(item.week).padStart(2, '0');
            if (exists) {
                scheduleHtml += '<li><span class="wk">' + weekStr + '</span>'
                    + '<a onclick="viewFile(\'' + item.file.substring(0, item.file.lastIndexOf('/')) + '\',\'' + item.file.split('/').pop() + '\')">' + escapeHtml(item.title) + '</a>'
                    + '<span class="status-dot ok">●</span></li>';
            } else {
                scheduleHtml += '<li><span class="wk">' + weekStr + '</span>'
                    + '<span style="color:var(--comment)">' + escapeHtml(item.title) + '</span>'
                    + '<span class="status-dot pending">○</span></li>';
            }
        });
        scheduleEl.innerHTML = scheduleHtml;

        // Progress: count labs and lectures dynamically
        var totalLectures = CONFIG.schedule.length;
        var lecturePct = Math.round((availableCount / totalLectures) * 100);

        var labDirs = tree['labs'] ? tree['labs'].dirs : [];
        var totalLabs = labDirs.length;
        var completedLabs = 0;
        labDirs.forEach(function (d) {
            var labPath = 'labs/' + d;
            var labNode = tree[labPath];
            if (labNode && (labNode.files.length > 0 || labNode.dirs.length > 0)) {
                completedLabs++;
            }
        });
        var labPct = totalLabs > 0 ? Math.round((completedLabs / totalLabs) * 100) : 0;

        progressEl.innerHTML =
            '<div style="display:flex;align-items:center;gap:6px;margin:4px 0;font-size:11px;">'
            + '<span class="output" style="min-width:55px">Lectures</span>'
            + '<div class="progress-bar" style="flex:1;height:12px;"><div class="progress-fill" style="width:' + lecturePct + '%"></div></div>'
            + '<span class="highlight" style="font-size:10px">' + availableCount + '/' + totalLectures + '</span>'
            + '</div>'
            + '<div style="display:flex;align-items:center;gap:6px;margin:4px 0;font-size:11px;">'
            + '<span class="output" style="min-width:55px">Labs</span>'
            + '<div class="progress-bar" style="flex:1;height:12px;"><div class="progress-fill" style="width:' + labPct + '%"></div></div>'
            + '<span class="highlight" style="font-size:10px">' + completedLabs + '/' + totalLabs + '</span>'
            + '</div>';
    }

    // ──────────────────────────────────────
    //  File Viewer
    // ──────────────────────────────────────
    function showBottomPane(title) {
        document.getElementById('viewer-placeholder').style.display = 'none';
        document.getElementById('viewer-title').textContent = title;
    }

    window.closeViewer = function () {
        document.getElementById('file-viewer').style.display = 'none';
        document.getElementById('file-viewer').innerHTML = '';
        document.getElementById('outline-content').style.display = 'none';
        document.getElementById('outline-content').innerHTML = '';
        document.getElementById('viewer-placeholder').style.display = 'flex';
        document.getElementById('viewer-title').textContent = 'bash — preview';
    };

    function renderFileView(filePath) {
        var viewerEl = document.getElementById('file-viewer');
        var outlineEl = document.getElementById('outline-content');
        outlineEl.style.display = 'none';

        var ext = getExt(filePath);
        var dirPath = filePath.split('/').slice(0, -1).join('/');
        var fileName = filePath.split('/').pop();

        showBottomPane('bash — cat ' + filePath);

        var html = '';
        if (ext === 'md') {
            var ghUrl = CONFIG.course.repoUrl + '/blob/main/' + filePath;
            html = '<div style="padding:6px 12px;background:rgba(0,255,65,0.04);border-bottom:1px solid var(--border);font-size:11px;flex-shrink:0;display:flex;align-items:center;gap:6px;">'
                + '<span style="color:var(--comment);">// navigation links may not work here —</span>'
                + '<a href="' + ghUrl + '" target="_blank" rel="noopener noreferrer" style="color:var(--cyan);text-decoration:none;border-bottom:1px dashed var(--cyan);transition:color 0.2s;">view on GitHub ↗</a>'
                + '</div>'
                + '<div class="md-viewer" id="md-render" style="max-height:none;flex:1;"></div>';
            viewerEl.innerHTML = html;
            viewerEl.style.display = 'flex';

            var container = document.getElementById('md-render');
            container.innerHTML = '<span style="color:var(--comment);font-style:italic">Loading...</span>';
            var baseDir = dirPath ? dirPath + '/' : '';

            fetch(filePath)
                .then(function (r) { if (!r.ok) throw new Error(); return r.text(); })
                .then(function (md) {
                    container.innerHTML = marked.parse(md);
                    // Rewrite relative paths for images and links
                    container.querySelectorAll('img[src], a[href]').forEach(function (el) {
                        var attr = el.hasAttribute('src') ? 'src' : 'href';
                        var val = el.getAttribute(attr);
                        if (val && !val.startsWith('http') && !val.startsWith('/') && !val.startsWith('#') && !val.startsWith('data:')) {
                            el.setAttribute(attr, baseDir + val);
                        }
                    });
                    // Handle anchor links
                    container.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
                        anchor.addEventListener('click', function (e) {
                            e.preventDefault();
                            var targetId = decodeURIComponent(this.getAttribute('href').slice(1));
                            var target = container.querySelector('[id="' + targetId.replace(/"/g, '\\"') + '"]');
                            if (!target) {
                                container.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(function (h) {
                                    if (h.id === targetId || h.id === targetId.toLowerCase()) target = h;
                                });
                            }
                            if (target) {
                                var scrollParent = container.closest('.pane-bottom') || container.closest('.terminal-body') || container;
                                var offset = target.getBoundingClientRect().top - scrollParent.getBoundingClientRect().top + scrollParent.scrollTop;
                                scrollParent.scrollTo({ top: offset - 10, behavior: 'smooth' });
                            }
                        });
                    });
                })
                .catch(function () { container.innerHTML = '<span style="color:var(--red)">Error loading file.</span>'; });
        } else if (ext === 'pdf') {
            html = '<iframe src="' + filePath + '" title="' + escapeHtml(fileName) + '"></iframe>';
            viewerEl.innerHTML = html;
            viewerEl.style.display = 'flex';
        } else if (['png', 'jpg', 'jpeg', 'gif', 'svg'].includes(ext)) {
            html = '<img src="' + filePath + '" alt="' + escapeHtml(fileName) + '">';
            viewerEl.innerHTML = html;
            viewerEl.style.display = 'flex';
        } else if (ext === 'html') {
            html = '<iframe src="' + filePath + '" title="' + escapeHtml(fileName) + '"></iframe>';
            viewerEl.innerHTML = html;
            viewerEl.style.display = 'flex';
        } else {
            html = '<div class="md-viewer" style="max-height:none;flex:1;"><span style="color:var(--comment)">Preview not available. <a href="' + filePath + '" target="_blank" style="color:var(--cyan)">Download file</a></span></div>';
            viewerEl.innerHTML = html;
            viewerEl.style.display = 'flex';
        }
    }

    // ──────────────────────────────────────
    //  Course Outline Viewer
    // ──────────────────────────────────────
    window.viewCourseOutline = function () {
        var viewerEl = document.getElementById('file-viewer');
        var container = document.getElementById('outline-content');
        viewerEl.style.display = 'none';
        viewerEl.innerHTML = '';
        showBottomPane('bash — cat course-outline.md');
        container.style.display = 'block';
        container.innerHTML = '<span style="color:#5c6370;font-style:italic">Loading...</span>';
        fetch('course-outline.md')
            .then(function (r) { return r.text(); })
            .then(function (md) { container.innerHTML = marked.parse(md); })
            .catch(function () { container.innerHTML = '<span style="color:#ff3e3e">Error loading file.</span>'; });
    };

    // ──────────────────────────────────────
    //  View Switch: Terminal ↔ README
    // ──────────────────────────────────────
    var currentView = 'terminal';

    window.switchView = function (view) {
        if (view === currentView) return;
        currentView = view;

        var terminalView = document.getElementById('terminal-view');
        var readmeView = document.getElementById('readme-view');
        var track = document.getElementById('toggle-track');
        var lblT = document.getElementById('lbl-terminal');
        var lblR = document.getElementById('lbl-readme');
        var matrixCanvas = document.getElementById('matrix-bg');

        if (view === 'readme') {
            terminalView.classList.add('hidden');
            readmeView.classList.add('active');
            track.classList.add('readme');
            lblT.classList.remove('active');
            lblR.classList.add('active');
            document.body.classList.add('readme-mode');
            document.body.style.background = '#f6f8fa';
            matrixCanvas.style.display = 'none';
            var container = document.getElementById('readme-content');
            if (!container.dataset.loaded) {
                container.innerHTML = '<p style="color:#656d76;font-style:italic">Loading...</p>';
                fetch('README.md')
                    .then(function (r) { return r.text(); })
                    .then(function (md) {
                        container.innerHTML = marked.parse(md);
                        container.dataset.loaded = '1';
                    })
                    .catch(function () { container.innerHTML = '<p style="color:#cf222e">Error loading README.md</p>'; });
            }
        } else {
            terminalView.classList.remove('hidden');
            readmeView.classList.remove('active');
            track.classList.remove('readme');
            lblT.classList.add('active');
            lblR.classList.remove('active');
            document.body.classList.remove('readme-mode');
            document.body.style.background = '';
            matrixCanvas.style.display = '';
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.toggleView = function () {
        window.switchView(currentView === 'terminal' ? 'readme' : 'terminal');
    };

    // ──────────────────────────────────────
    //  Explorer Navigation
    // ──────────────────────────────────────
    window.enterExplorer = function () {
        if (!Presence.isLoggedIn()) return;
        document.getElementById('landing-page').classList.add('hidden');
        document.getElementById('contents-page').classList.add('active');
        renderExplorer('');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.backToLanding = function () {
        document.getElementById('contents-page').classList.remove('active');
        document.getElementById('landing-page').classList.remove('hidden');
        window.location.hash = '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Enter'
            && !document.getElementById('landing-page').classList.contains('hidden')
            && Presence.isLoggedIn()) {
            enterExplorer();
        }
    });

    // ──────────────────────────────────────
    //  Hash Router
    // ──────────────────────────────────────
    function handleHash() {
        var hash = window.location.hash.slice(1);
        if (hash === 'admin') {
            renderAdminPanel();
        } else if (hash === 'grades') {
            renderStudentGrades();
        } else if (hash.startsWith('browse/') || hash === 'browse') {
            var path = hash === 'browse' ? '' : hash.slice(7);
            renderExplorer(path);
        } else if (hash.startsWith('view/')) {
            var filePath = hash.slice(5);
            renderFileView(filePath);
        } else if (hash === 'readme') {
            window.switchView('readme');
        }
    }

    window.addEventListener('hashchange', handleHash);

    // ──────────────────────────────────────
    //  Layout Toggle
    // ──────────────────────────────────────
    var layoutMode = 'horizontal';

    window.toggleLayout = function () {
        var splitPane = document.querySelector('.split-pane');
        var paneTop = document.getElementById('pane-top');
        var btns = document.querySelectorAll('.layout-toggle');

        paneTop.style.flex = '';
        paneTop.style.height = '';
        paneTop.style.width = '';

        if (layoutMode === 'vertical') {
            layoutMode = 'horizontal';
            splitPane.classList.add('side-view');
            btns.forEach(function (b) { b.innerHTML = '<span class="icon">⬌</span> split'; b.title = 'Toggle top/bottom view'; });
        } else {
            layoutMode = 'vertical';
            splitPane.classList.remove('side-view');
            btns.forEach(function (b) { b.innerHTML = '<span class="icon">⬍</span> split'; b.title = 'Toggle side view'; });
        }
    };

    // ──────────────────────────────────────
    //  Split Pane Resize
    // ──────────────────────────────────────
    (function () {
        var divider = document.getElementById('pane-divider');
        var paneTop = document.getElementById('pane-top');
        if (!divider || !paneTop) return;
        var splitPane = paneTop.parentElement;
        var isDragging = false;

        divider.addEventListener('mousedown', function (e) {
            e.preventDefault();
            isDragging = true;
            divider.classList.add('active');
            document.body.style.cursor = layoutMode === 'horizontal' ? 'col-resize' : 'row-resize';
            document.body.style.userSelect = 'none';
        });

        document.addEventListener('mousemove', function (e) {
            if (!isDragging) return;
            var rect = splitPane.getBoundingClientRect();
            var minPx = layoutMode === 'horizontal' ? 200 : 80;

            if (layoutMode === 'horizontal') {
                var offset = e.clientX - rect.left;
                var total = rect.width;
                var clamped = Math.max(minPx, Math.min(offset, total - minPx - 5));
                paneTop.style.flex = 'none';
                paneTop.style.width = clamped + 'px';
                paneTop.style.height = '';
            } else {
                var offset = e.clientY - rect.top;
                var total = rect.height;
                var clamped = Math.max(minPx, Math.min(offset, total - minPx - 5));
                paneTop.style.flex = 'none';
                paneTop.style.height = clamped + 'px';
                paneTop.style.width = '';
            }
        });

        document.addEventListener('mouseup', function () {
            if (!isDragging) return;
            isDragging = false;
            divider.classList.remove('active');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        });
    })();

    // ──────────────────────────────────────
    //  Mobile Sidebar
    // ──────────────────────────────────────
    window.toggleMobileSidebar = function () {
        document.getElementById('sidebar').classList.toggle('open');
        document.getElementById('mobile-sidebar-overlay').classList.toggle('visible');
    };

    window.closeMobileSidebar = function () {
        document.getElementById('sidebar').classList.remove('open');
        document.getElementById('mobile-sidebar-overlay').classList.remove('visible');
    };

    document.querySelectorAll('.sidebar-nav li, .sidebar-schedule a, .sidebar-back').forEach(function (el) {
        el.addEventListener('click', window.closeMobileSidebar);
    });

    // ──────────────────────────────────────
    //  Scroll Reveal & Progress Animations
    // ──────────────────────────────────────
    var revealElements = document.querySelectorAll('.reveal');
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.1 });
    revealElements.forEach(function (el) { observer.observe(el); });

    var progressBars = document.querySelectorAll('.progress-fill');
    var progressObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var width = entry.target.style.width;
                entry.target.style.width = '0%';
                setTimeout(function () { entry.target.style.width = width; }, 200);
            }
        });
    }, { threshold: 0.5 });
    progressBars.forEach(function (bar) { progressObserver.observe(bar); });

    // ──────────────────────────────────────
    //  Init
    // ──────────────────────────────────────
    var hash = window.location.hash.slice(1);
    if (hash.startsWith('browse') || hash.startsWith('view') || hash === 'readme') {
        enterExplorer();
        handleHash();
    }
})();
