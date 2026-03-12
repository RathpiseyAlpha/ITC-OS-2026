/* ═══════════════════════════════════════════════════════
   ITC-OS-2026 — Shared Terminal JS (scroll reveal + md rendering)
   ═══════════════════════════════════════════════════════ */

// ─── Scroll Reveal ───
document.addEventListener('DOMContentLoaded', () => {
    const revealEls = document.querySelectorAll('.reveal');
    const obs = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
    }, { threshold: 0.1 });
    revealEls.forEach(el => obs.observe(el));
});

// ─── Lightweight Markdown → HTML renderer ───
function renderMarkdown(md) {
    let html = md;

    // Code blocks (fenced)
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
        const escaped = code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        return '<pre><code class="lang-' + (lang||'text') + '">' + escaped + '</code></pre>';
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Images
    html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img alt="$1" src="$2">');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Headers
    html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Horizontal rules
    html = html.replace(/^---+$/gm, '<hr>');

    // Bold & italic
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Blockquotes
    html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

    // Unordered lists
    html = html.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Tables (basic)
    html = html.replace(/^\|(.+)\|$/gm, (match) => {
        const cells = match.split('|').filter(c => c.trim() !== '');
        if (cells.every(c => /^[\s\-:]+$/.test(c))) return ''; // separator row
        const isHeader = false;
        const tag = 'td';
        return '<tr>' + cells.map(c => '<' + tag + '>' + c.trim() + '</' + tag + '>').join('') + '</tr>';
    });
    html = html.replace(/(<tr>.*<\/tr>\n?)+/g, '<table>$&</table>');

    // Paragraphs — wrap remaining loose text lines
    html = html.replace(/^(?!<[a-z/])(.*\S.*)$/gm, '<p>$1</p>');

    // Clean up empty paragraphs
    html = html.replace(/<p>\s*<\/p>/g, '');

    return html;
}

// ─── Load and render a .md file into a container ───
function loadMarkdownFile(url, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '<span class="comment">Loading...</span>';
    fetch(url)
        .then(r => {
            if (!r.ok) throw new Error('File not found');
            return r.text();
        })
        .then(md => {
            container.innerHTML = renderMarkdown(md);
        })
        .catch(() => {
            container.innerHTML = '<span class="error">Error: Could not load file.</span>';
        });
}
