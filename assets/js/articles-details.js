const params = new URLSearchParams(window.location.search);
const requestedFileName = params.get('file');
const pageTitle = params.get('title');

function normalizeArticleFileName(fileName) {
    return fileName.endsWith('.tex') ? `${fileName.slice(0, -4)}.html` : fileName;
}

async function loadArticle() {
    const targetDiv = document.getElementById('article-content');
    const titleElement = document.getElementById('display-title');

    if (pageTitle) {
        titleElement.textContent = pageTitle;
        document.title = `${pageTitle} | yura1685`;
    }

    if (!requestedFileName) {
        targetDiv.textContent = 'ファイルが指定されていません。';
        return;
    }

    const fileName = normalizeArticleFileName(requestedFileName);
    if (!/^[A-Za-z0-9_-]+\.html$/.test(fileName)) {
        targetDiv.textContent = '不正なファイル名です。';
        return;
    }

    try {
        const response = await fetch(`./contents/${fileName}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const text = await response.text();
        targetDiv.innerHTML = text;

        targetDiv.querySelectorAll('a[href^="http"]').forEach(link => {
            if (link.target === '_blank') link.rel = 'noopener noreferrer';
        });

        targetDiv.querySelectorAll('pre code').forEach(codeBlock => {
            codeBlock.textContent = codeBlock.textContent.trim();
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
