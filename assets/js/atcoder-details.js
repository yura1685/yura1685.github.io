const params = new URLSearchParams(window.location.search);
const fileName = params.get('file');

function setCanonicalUrl(file) {
    const canonical = document.getElementById('canonical-link');
    if (!canonical) return;

    const url = new URL(window.location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('file', file);
    canonical.href = url.href;
}

async function loadArticle() {
    const targetDiv = document.getElementById('markdown-content');
    if (!fileName) {
        targetDiv.textContent = 'ファイルが指定されていません。';
        return;
    }

    // solutions以下のMarkdown以外は読み込まない
    if (!/^[A-Za-z0-9_-]+\.md$/.test(fileName)) {
        targetDiv.textContent = '不正なファイル名です。';
        return;
    }

    setCanonicalUrl(fileName);

    try {
        const response = await fetch(`./solutions/${fileName}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const markdown = await response.text();

        // Markdown先頭のH1をページタイトルにも反映する
        const heading = markdown.match(/^#\s+(.+)$/m)?.[1]?.trim();
        if (heading) document.title = `${heading} | yura1685`;

        targetDiv.innerHTML = marked.parse(markdown);

        // 外部リンクは別タブで開く
        targetDiv.querySelectorAll('a[href^="http"]').forEach(link => {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
        });

        if (window.MathJax && window.MathJax.typesetPromise) {
            await window.MathJax.typesetPromise([targetDiv]);
        }
        if (window.Prism) {
            Prism.highlightAllUnder(targetDiv);
        }
    } catch (error) {
        targetDiv.textContent = '記事の読み込みに失敗しました。';
        console.error(error);
    }
}

loadArticle();
