const params = new URLSearchParams(window.location.search);
const fileName = params.get('file');

async function loadArticle() {
    const targetDiv = document.getElementById('markdown-content');
    if (!fileName) {
        targetDiv.textContent = 'ファイルが指定されていません。';
        return;
    }

    if (!/^[A-Za-z0-9_-]+\.md$/.test(fileName)) {
        targetDiv.textContent = '不正なファイル名です。';
        return;
    }

    setCanonicalUrl(fileName);

    try {
        const response = await fetch(`./solutions/${fileName}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const markdown = await response.text();

        const heading = markdown.match(/^#\s+(.+)$/m)?.[1]?.trim();
        if (heading) document.title = `${heading} | yura1685`;

        renderMarkdown(targetDiv, markdown);
        await finishMarkdown(targetDiv);
    } catch (error) {
        targetDiv.textContent = '記事の読み込みに失敗しました。';
        console.error(error);
    }
}

loadArticle();
