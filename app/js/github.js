// ─── GitHub API: Dynamic Repository Tree ───
// Fetches the actual file structure from GitHub instead of a hardcoded manifest.

const GitHubAPI = (function () {
    const CACHE_KEY = 'itc-os-repo-tree-v4';
    const CACHE_TS_KEY = 'itc-os-repo-tree-ts-v4';

    // Top-level entries hidden from the file browser (tooling/config/app source).
    const HIDDEN_TOP = ['.claude', '.github', '.vscode', 'app', '.gitignore', '.nojekyll'];

    let fileTree = null; // { '': { dirs: [], files: [] }, 'labs': {...}, ... }
    let allFiles = null; // Set of all file paths for existence checks

    // Generated snapshot of the repo file list, used only when the GitHub API is
    // unreachable (e.g. the unauthenticated 60/hr rate limit) AND nothing is cached.
    // The live API supersedes this whenever it succeeds; regenerate with:
    //   git ls-files
    const FALLBACK_PATHS = [
        ".claude/settings.local.json", ".github/workflows/deploy.yml", ".gitignore", ".nojekyll", ".vscode/settings.json", "README.md",
        "app/css/2d92accdc77f74ad3949c6edb5b49686.gif", "app/css/penguin-walking-transparent-big.gif", "app/css/running-pose-only-transparent.gif", "app/css/styles.css", "app/js/app.js", "app/js/config.js",
        "app/js/env.example.js", "app/js/github.js", "app/js/presence.js", "app/server/.dockerignore", "app/server/Dockerfile", "app/server/README.md",
        "app/server/app.py", "app/server/auto-deploy.sh", "app/server/docker-compose.yml", "app/server/itc-os-presence.service", "app/server/requirements.txt", "course-outline.md",
        "index.html", "labs/lab1/README.md", "labs/lab1/guides/images/page12_img0.png", "labs/lab1/guides/images/page15_img0.png", "labs/lab1/guides/images/page1_img0.png", "labs/lab1/guides/images/page2_img0.png",
        "labs/lab1/guides/images/page4_img0.png", "labs/lab1/guides/images/page4_img1.jpg", "labs/lab1/guides/images/page4_img2.png", "labs/lab1/guides/images/page4_img3.png", "labs/lab1/guides/images/page5_img0.png", "labs/lab1/guides/images/page6_img0.png",
        "labs/lab1/guides/images/page7_img0.png", "labs/lab1/guides/images/page8_img0.jpg", "labs/lab1/guides/lab1-guides.pdf", "labs/lab1/guides/slides.html", "labs/lab1/lab1-instruction.md", "labs/lab1/pictures/image.png",
        "labs/lab1/pictures/lab-workflow.png", "labs/lab2/README.md", "labs/lab2/guides/images/page10_img0.png", "labs/lab2/guides/images/page11_img0.png", "labs/lab2/guides/images/page12_img0.png", "labs/lab2/guides/images/page12_img1.png",
        "labs/lab2/guides/images/page13_img0.png", "labs/lab2/guides/images/page13_img1.png", "labs/lab2/guides/images/page14_img0.png", "labs/lab2/guides/images/page14_img1.png", "labs/lab2/guides/images/page15_img0.png", "labs/lab2/guides/images/page15_img1.png",
        "labs/lab2/guides/images/page17_img0.png", "labs/lab2/guides/images/page1_img0.png", "labs/lab2/guides/images/page3_img0.jpeg", "labs/lab2/guides/images/page4_img0.png", "labs/lab2/guides/images/page5_img0.png", "labs/lab2/guides/images/page5_img1.png",
        "labs/lab2/guides/images/page6_img0.png", "labs/lab2/guides/images/page7_img0.png", "labs/lab2/guides/images/page8_img0.png", "labs/lab2/guides/images/page9_img0.png", "labs/lab2/guides/images/page9_img1.png", "labs/lab2/guides/lab2-guides.pdf",
        "labs/lab2/guides/slides.html", "labs/lab2/lab2-instruction.md", "labs/lab3/README.md", "labs/lab3/guides/slides.html", "labs/lab3/lab3-instruction.md", "labs/lab4/README.md",
        "labs/lab4/guides/slides.html", "labs/lab4/lab4-challenge.md", "labs/lab4/lab4-instruction.md", "labs/lab5/README.md", "labs/lab5/guides/slides.html", "labs/lab5/lab5-instruction.md",
        "labs/lab6/README.md", "labs/lab6/guides/slides.html", "labs/lab6/lab6-instruction.md", "labs/lab7/README.md", "labs/lab7/lab7-instruction.md", "labs/lab8/README.md",
        "labs/lab8/lab8-instruction.md", "labs/lab9/README.md", "labs/lab9/lab9-instruction.md", "lectures/class-activity/README.md", "lectures/class-activity/class-activity1.md", "lectures/class-activity/class-activity1.pdf",
        "lectures/class-activity/class-activity2.md", "lectures/class-activity/class-activity3.md", "lectures/class-activity/class-activity4.md", "lectures/class-activity/class-activity5.md", "lectures/class-activity/class-activity6.md", "lectures/class-activity/class-activity7.md",
        "lectures/class-activity/class-activity8.md", "lectures/files/ch1.pdf", "lectures/files/ch10.pdf", "lectures/files/ch2.pdf", "lectures/files/ch3.pdf", "lectures/files/ch4.pdf",
        "lectures/files/ch5.pdf", "lectures/files/ch6.pdf", "lectures/files/ch7.pdf", "lectures/files/ch8.pdf", "lectures/files/ch9.pdf", "lectures/notes/README.md",
        "lectures/notes/week01-introduction-to-os.md", "lectures/notes/week02-os-structures-interfaces.md", "lectures/notes/week03-processes.md", "lectures/notes/week04-threads-multicore.md", "lectures/notes/week05-cpu-scheduling-1.md", "lectures/notes/week06-cpu-scheduling-2.md",
        "lectures/notes/week07-critical-sections.md", "lectures/notes/week08-semaphores-sync.md", "lectures/notes/week09-deadlocks.md", "lectures/notes/week10-memory-management.md", "lectures/notes/week11-virtual-memory.md", "lectures/notes/week12-file-systems.md",
        "lectures/visualizations/README.md", "lectures/visualizations/bankers-algorithm.html", "lectures/visualizations/deadlock-detection.html", "lectures/visualizations/index.html", "lectures/visualizations/rag-deadlock.html", "tools/create-2026-expanded-qbank.ps1",
        "tools/fix-linux-tree-prompts.ps1", "tools/preview-moodle-qbank.ps1", "tools/revise-linux-qbank-and-add-lecture-short.ps1"
    ];

    // Persisted cache (localStorage so it survives reloads/new tabs, unlike sessionStorage).
    function readCache() {
        try {
            const raw = localStorage.getItem(CACHE_KEY);
            if (!raw) return null;
            const parsed = JSON.parse(raw);
            if (!parsed || !parsed.tree) return null;
            return {
                tree: parsed.tree,
                files: new Set(parsed.files || []),
                ts: parseInt(localStorage.getItem(CACHE_TS_KEY) || '0', 10)
            };
        } catch (e) {
            return null;
        }
    }
    function writeCache(tree, files) {
        try {
            localStorage.setItem(CACHE_KEY, JSON.stringify({ tree: tree, files: Array.from(files) }));
            localStorage.setItem(CACHE_TS_KEY, String(Date.now()));
        } catch (e) {
            /* storage disabled or full — non-fatal */
        }
    }

    // Build the hierarchical tree from a flat list of paths
    function buildTree(entries) {
        const tree = {};
        const dirs = new Set();
        const fileSet = new Set();

        // Drop hidden tooling/config directories (and their contents).
        entries = entries.filter(e => HIDDEN_TOP.indexOf(e.path.split('/')[0]) === -1);

        // Collect all directories (including implicit parents)
        entries.forEach(e => {
            if (e.type === 'tree') {
                dirs.add(e.path);
            } else if (e.type === 'blob') {
                fileSet.add(e.path);
                // Ensure parent dirs exist
                const parts = e.path.split('/');
                for (let i = 1; i < parts.length; i++) {
                    dirs.add(parts.slice(0, i).join('/'));
                }
            }
        });

        // Root entry
        tree[''] = { dirs: [], files: [] };

        // Initialize all directories
        dirs.forEach(d => {
            tree[d] = { dirs: [], files: [] };
        });

        // Populate directories with their children
        dirs.forEach(d => {
            const parent = d.includes('/') ? d.substring(0, d.lastIndexOf('/')) : '';
            const name = d.includes('/') ? d.substring(d.lastIndexOf('/') + 1) : d;
            if (tree[parent]) {
                tree[parent].dirs.push(name);
            }
        });

        // Populate files
        fileSet.forEach(f => {
            const parent = f.includes('/') ? f.substring(0, f.lastIndexOf('/')) : '';
            const name = f.includes('/') ? f.substring(f.lastIndexOf('/') + 1) : f;
            if (tree[parent]) {
                tree[parent].files.push({ name: name });
            }
        });

        // Sort dirs and files alphabetically in each node
        Object.keys(tree).forEach(key => {
            tree[key].dirs.sort((a, b) => a.localeCompare(b));
            tree[key].files.sort((a, b) => a.name.localeCompare(b.name));
        });

        return { tree, fileSet };
    }

    // Fetch tree from GitHub API
    async function fetchTree() {
        const { owner, repo, branch, token } = CONFIG.github;
        const url = `https://api.github.com/repos/${owner}/${repo}/git/trees/${branch}?recursive=1`;

        const headers = { 'Accept': 'application/vnd.github.v3+json' };
        if (token) {
            headers['Authorization'] = `token ${token}`;
        }

        const response = await fetch(url, { headers });
        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const data = await response.json();
        return data.tree; // Array of { path, type, sha, size, ... }
    }

    // Get tree, using cache if available
    async function getTree() {
        if (fileTree) return fileTree;

        const cached = readCache();

        // Fresh cache → use directly, no network call
        if (cached && (Date.now() - cached.ts) < CONFIG.cacheDuration) {
            fileTree = cached.tree;
            allFiles = cached.files;
            return fileTree;
        }

        // Fetch from API
        try {
            const entries = await fetchTree();
            const result = buildTree(entries);
            fileTree = result.tree;
            allFiles = result.fileSet;
            writeCache(fileTree, allFiles);
            return fileTree;
        } catch (err) {
            console.warn('GitHub API fetch failed:', err.message);
            // Prefer the last successfully-fetched tree (even if stale) over the
            // static fallback — it is the real, complete structure.
            if (cached) {
                console.warn('Using last cached repo tree from', new Date(cached.ts).toLocaleString());
                fileTree = cached.tree;
                allFiles = cached.files;
                return fileTree;
            }
            return getFallbackTree();
        }
    }

    // Check if a file exists in the repo
    function fileExists(path) {
        return allFiles ? allFiles.has(path) : false;
    }

    // Get all file paths
    function getAllFiles() {
        return allFiles ? allFiles : new Set();
    }

    // Count items in a directory path
    function getNodeInfo(path) {
        if (!fileTree || !fileTree[path]) return null;
        const node = fileTree[path];
        return {
            dirCount: node.dirs.length,
            fileCount: node.files.length,
            total: node.dirs.length + node.files.length
        };
    }

    // Complete fallback tree built from the embedded snapshot (used only if the
    // API fails and nothing is cached). Covers the full repo, incl. visualizations.
    function getFallbackTree() {
        const entries = FALLBACK_PATHS.map(p => ({ path: p, type: 'blob' }));
        const result = buildTree(entries);
        fileTree = result.tree;
        allFiles = result.fileSet;
        return fileTree;
    }

    // Force refresh the cache
    async function refresh() {
        try {
            localStorage.removeItem(CACHE_KEY);
            localStorage.removeItem(CACHE_TS_KEY);
        } catch (e) { /* ignore */ }
        fileTree = null;
        allFiles = null;
        return getTree();
    }

    return {
        getTree,
        fileExists,
        getAllFiles,
        getNodeInfo,
        refresh
    };
})();
