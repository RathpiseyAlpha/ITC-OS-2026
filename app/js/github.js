// ─── GitHub API: Dynamic Repository Tree ───
// Fetches the actual file structure from GitHub instead of a hardcoded manifest.

const GitHubAPI = (function () {
    const CACHE_KEY = 'itc-os-repo-tree';
    const CACHE_TS_KEY = 'itc-os-repo-tree-ts';

    let fileTree = null; // { '': { dirs: [], files: [] }, 'labs': {...}, ... }
    let allFiles = null; // Set of all file paths for existence checks

    // Build the hierarchical tree from a flat list of paths
    function buildTree(entries) {
        const tree = {};
        const dirs = new Set();
        const fileSet = new Set();

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

        // Check sessionStorage cache
        const cached = sessionStorage.getItem(CACHE_KEY);
        const cachedTs = sessionStorage.getItem(CACHE_TS_KEY);

        if (cached && cachedTs && (Date.now() - parseInt(cachedTs)) < CONFIG.cacheDuration) {
            const parsed = JSON.parse(cached);
            fileTree = parsed.tree;
            allFiles = new Set(parsed.files);
            return fileTree;
        }

        // Fetch from API
        try {
            const entries = await fetchTree();
            const result = buildTree(entries);
            fileTree = result.tree;
            allFiles = result.fileSet;

            // Cache
            sessionStorage.setItem(CACHE_KEY, JSON.stringify({
                tree: fileTree,
                files: Array.from(allFiles)
            }));
            sessionStorage.setItem(CACHE_TS_KEY, String(Date.now()));

            return fileTree;
        } catch (err) {
            console.warn('GitHub API fetch failed, using fallback:', err.message);
            // Return a minimal fallback
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

    // Minimal fallback tree (used if API fails)
    function getFallbackTree() {
        fileTree = {
            '': {
                dirs: ['labs', 'lectures'],
                files: [
                    { name: 'README.md' },
                    { name: 'course-outline.md' },
                    { name: 'index.html' }
                ]
            },
            'labs': { dirs: ['lab1', 'lab2', 'lab3'], files: [] },
            'lectures': { dirs: ['files', 'notes', 'class-activity'], files: [] }
        };
        allFiles = new Set(['README.md', 'course-outline.md', 'index.html']);
        return fileTree;
    }

    // Force refresh the cache
    async function refresh() {
        sessionStorage.removeItem(CACHE_KEY);
        sessionStorage.removeItem(CACHE_TS_KEY);
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
