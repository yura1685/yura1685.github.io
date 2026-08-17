const ARTICLE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1417312107&single=true&output=csv";
const params = new URLSearchParams(window.location.search);
const requestedFileName = params.get('file');
const legacyPageTitle = params.get('title');

function setCanonicalUrl(fileName) {
    const canonical = document.getElementById('canonical-link');
    if (!canonical) return;

    const url = new URL(window.location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('file', fileName);
    canonical.href = url.href;
}

async function loadArticleMetadata(fileName) {
    try {
        const response = await fetch(ARTICLE_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText);
        if (rows.length === 0) return null;

        const header = rows[0].map(value => value.trim().toLowerCase());
        const titleIndex = header.indexOf('title');
        const fileIndex = header.indexOf('file');
        const descIndex = header.indexOf('description') !== -1
            ? header.indexOf('description')
            : header.indexOf('desc');

        if (titleIndex === -1 || fileIndex === -1) return null;

        const row = rows.slice(1).find(cols => (cols[fileIndex] || '').trim() === fileName);
        if (!row) return null;

        return {
            title: (row[titleIndex] || '').trim(),
            desc: descIndex === -1 ? '' : (row[descIndex] || '').trim()
        };
    } catch (error) {
        console.error('Failed to load article metadata.', error);
        return null;
    }
}

async function loadArticle() {
    const targetDiv = document.getElementById('article-content');
    const titleElement = document.getElementById('display-title');
    const descriptionElement = document.getElementById('page-description');

    if (!requestedFileName) {
        titleElement.textContent = 'Article';
        targetDiv.textContent = 'ファイルが指定されていません。';
        return;
    }

    // contents以下のMarkdown以外は読み込まない
    if (!/^[A-Za-z0-9_-]+\.md$/.test(requestedFileName)) {
        titleElement.textContent = 'Article';
        targetDiv.textContent = '不正なファイル名です。';
        return;
    }

    setCanonicalUrl(requestedFileName);

    // Blogなど、titleパラメータを持たないリンクからでもタイトルを表示できるようにする
    const metadataPromise = loadArticleMetadata(requestedFileName);

    try {
        const response = await fetch(`./contents/${requestedFileName}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const markdown = await response.text();
        targetDiv.innerHTML = marked.parse(markdown);

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

    const metadata = await metadataPromise;
    const title = metadata?.title || legacyPageTitle || 'Article';
    titleElement.textContent = title;
    document.title = `${title} | yura1685`;

    if (descriptionElement && metadata?.desc) {
        descriptionElement.content = metadata.desc;
    }
}

loadArticle();
