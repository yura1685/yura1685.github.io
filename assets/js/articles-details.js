const params = new URLSearchParams(window.location.search);
const requestedFileName = params.get('file');
const legacyPageTitle = params.get('title');

async function loadArticleMetadata(fileName) {
    try {
        const response = await fetch(SHEET_ARTICLES_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const articles = parseArticlesCSV(await response.text());
        return articles.find(article => article.file === fileName) || null;
    } catch (error) {
        console.error('Failed to load article metadata.', error);
        return null;
    }
}

function renderArticleMetadata(metadata) {
    const meta = document.getElementById('article-meta');
    const dateElement = document.getElementById('article-date');
    const tagsElement = document.getElementById('article-meta-tags');
    if (!meta || !dateElement || !tagsElement || !metadata) return;

    dateElement.textContent = metadata.date;
    dateElement.hidden = !metadata.date;
    tagsElement.replaceChildren();

    metadata.tags.forEach(tag => {
        const link = document.createElement('a');
        link.className = 'tag-badge article-meta-tag';
        link.href = `index.html?tag=${encodeURIComponent(tag)}`;
        link.textContent = tag;
        tagsElement.appendChild(link);
    });

    meta.hidden = !metadata.date && metadata.tags.length === 0;
}

function makeHeadingId(text, index, usedIds) {
    let id = text.normalize('NFKC')
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '-')
        .replace(/[^\p{Letter}\p{Number}_-]/gu, '')
        .replace(/^-+|-+$/g, '');

    if (!id) id = `section-${index + 1}`;

    const base = id;
    let suffix = 2;
    while (usedIds.has(id)) {
        id = `${base}-${suffix}`;
        suffix++;
    }
    usedIds.add(id);
    return id;
}

function buildTableOfContents(targetDiv) {
    const toc = document.getElementById('article-toc');
    const tocList = document.getElementById('article-toc-list');
    if (!toc || !tocList) return;

    const headings = [...targetDiv.querySelectorAll('h1, h2, h3')];
    tocList.replaceChildren();

    if (headings.length === 0) {
        toc.hidden = true;
        return;
    }

    const usedIds = new Set();
    headings.forEach((heading, index) => {
        const headingText = heading.textContent.trim();
        if (!headingText) return;

        if (!heading.id || usedIds.has(heading.id)) {
            heading.id = makeHeadingId(headingText, index, usedIds);
        } else {
            usedIds.add(heading.id);
        }

        const item = document.createElement('li');
        item.className = `toc-level-${heading.tagName.substring(1)}`;

        const link = document.createElement('a');
        link.href = `#${encodeURIComponent(heading.id)}`;
        link.textContent = headingText;

        item.appendChild(link);
        tocList.appendChild(item);
    });

    toc.hidden = tocList.children.length === 0;
}

// X のポスト埋め込みがある記事だけ widgets.js を読み込む（読み込み後に自動で表示される）
function renderTwitterEmbeds(targetDiv) {
    targetDiv.querySelectorAll('script[src*="platform.x.com/widgets.js"], script[src*="platform.twitter.com/widgets.js"]').forEach(script => script.remove());

    if (!targetDiv.querySelector('.twitter-tweet')) return;

    const script = document.createElement('script');
    script.src = 'https://platform.x.com/widgets.js';
    script.async = true;
    script.charset = 'utf-8';
    document.body.appendChild(script);
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

    if (!/^[A-Za-z0-9_-]+\.md$/.test(requestedFileName)) {
        titleElement.textContent = 'Article';
        targetDiv.textContent = '不正なファイル名です。';
        return;
    }

    setCanonicalUrl(requestedFileName);

    const metadataPromise = loadArticleMetadata(requestedFileName);

    try {
        const response = await fetch(`./contents/${requestedFileName}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        renderMarkdown(targetDiv, await response.text());
        buildTableOfContents(targetDiv);
        renderTwitterEmbeds(targetDiv);
        await finishMarkdown(targetDiv);
    } catch (error) {
        targetDiv.textContent = '記事の読み込みに失敗しました。';
        console.error(error);
    }

    const metadata = await metadataPromise;
    const title = metadata?.title || legacyPageTitle || 'Article';
    titleElement.textContent = title;
    document.title = `${title} | yura1685`;

    renderArticleMetadata(metadata);

    if (descriptionElement && metadata?.desc) {
        descriptionElement.content = metadata.desc;
    }
}

loadArticle();
