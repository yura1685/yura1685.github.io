const params = new URLSearchParams(window.location.search);
const fileName = params.get('file');

async function loadArticle() {
    const targetDiv = document.getElementById('markdown-content');
    if (!fileName) {
        targetDiv.innerText = 'ファイルが指定されていません。';
        return;
    }

    // solutions 以下の Markdown 以外は読み込まない
    if (!/^[A-Za-z0-9_-]+\.md$/.test(fileName)) {
        targetDiv.innerText = '不正なファイル名です。';
        return;
    }

    try {
        const response = await fetch(`./solutions/${fileName}`);
        if (!response.ok) throw new Error('Not found');
        const markdown = await response.text();

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
    } catch (e) {
        targetDiv.innerText = '記事の読み込みに失敗しました。';
    }
}

loadArticle();
