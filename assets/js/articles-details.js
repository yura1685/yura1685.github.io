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

        // 修正: 列順に依存せず、日付・タグも取得する
        const header = rows[0].map(value => value.trim().toLowerCase());
        const dateIndex = header.indexOf('date');
        const titleIndex = header.indexOf('title');
        const tagsIndex = header.indexOf('tags') !== -1 ? header.indexOf('tags') : header.indexOf('tag');
        const fileIndex = header.indexOf('file');
        const descIndex = header.indexOf('description') !== -1
            ? header.indexOf('description')
            : header.indexOf('desc');

        if (titleIndex === -1 || fileIndex === -1) return null;

        const row = rows.slice(1).find(cols => (cols[fileIndex] || '').trim() === fileName);
        if (!row) return null;

        return {
            date: dateIndex === -1 ? '' : (row[dateIndex] || '').trim(),
            title: (row[titleIndex] || '').trim(),
            tags: tagsIndex === -1 ? [] : (row[tagsIndex] || '').split('|').map(tag => tag.trim()).filter(Boolean),
            desc: descIndex === -1 ? '' : (row[descIndex] || '').trim()
        };
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

    // h4の「解法」など細かすぎる見出しは除外する
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

function renderTwitterEmbeds(targetDiv) {
    // 古いMarkdownにscriptが残っていても二重読込しない
    targetDiv.querySelectorAll('script[src*="platform.x.com/widgets.js"], script[src*="platform.twitter.com/widgets.js"]').forEach(script => script.remove());

    if (!targetDiv.querySelector('.twitter-tweet')) return;

    const loadWidgets = () => {
        if (window.twttr?.widgets?.load) {
            window.twttr.widgets.load(targetDiv);
        }
    };

    if (window.twttr?.widgets?.load) {
        loadWidgets();
        return;
    }

    const script = document.getElementById('twitter-wjs');
    if (script) script.addEventListener('load', loadWidgets, { once: true });
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

        // 修正: 見出しから目次を生成し、X埋め込みを本文挿入後に明示的に描画
        buildTableOfContents(targetDiv);
        renderTwitterEmbeds(targetDiv);

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

    renderArticleMetadata(metadata);

    if (descriptionElement && metadata?.desc) {
        descriptionElement.content = metadata.desc;
    }
}

loadArticle();
