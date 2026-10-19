let allArticles = [];

async function loadArticles() {
    const list = document.getElementById('article-list');

    try {
        const response = await fetch(SHEET_ARTICLES_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        allArticles = parseArticlesCSV(await response.text())
            .filter(article => article.date)
            .sort((a, b) => b.date.localeCompare(a.date));

        const initialTag = new URLSearchParams(window.location.search).get('tag');
        if (initialTag) {
            document.getElementById('tag-filter').value = initialTag;
            filterArticles(true);
        } else {
            displayArticles(allArticles);
        }
    } catch (error) {
        list.textContent = '記事一覧の読み込みに失敗しました。';
        console.error('Failed to load articles.', error);
    }
}

function displayArticles(articles) {
    const list = document.getElementById('article-list');
    list.replaceChildren();

    if (articles.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.textContent = '条件に一致する記事がありません。';
        list.appendChild(empty);
        return;
    }

    articles.forEach(article => {
        const card = document.createElement('article');
        card.className = 'article-card';

        const mainLink = document.createElement('a');
        mainLink.className = 'article-card-link';
        mainLink.href = `details.html?file=${encodeURIComponent(article.file)}`;

        const date = document.createElement('div');
        date.className = 'article-date';
        date.textContent = article.date;

        const title = document.createElement('div');
        title.className = 'article-title';
        title.textContent = article.title;

        const desc = document.createElement('p');
        desc.className = 'article-desc';
        desc.textContent = article.desc;

        mainLink.append(date, title, desc);

        const tags = document.createElement('div');
        tags.className = 'article-tags';
        article.tags.forEach(tag => {
            const badge = document.createElement('button');
            badge.type = 'button';
            badge.className = 'tag-badge tag-button';
            badge.textContent = tag;
            badge.onclick = () => {
                document.getElementById('tag-filter').value = tag;
                history.replaceState(null, '', `?tag=${encodeURIComponent(tag)}`);
                filterArticles(true);
            };
            tags.appendChild(badge);
        });

        card.append(mainLink, tags);
        list.appendChild(card);
    });
}

function filterArticles(keepTagParam = false) {
    const query = document.getElementById('tag-filter').value.trim().toLowerCase();
    const filtered = allArticles.filter(article =>
        article.tags.join('|').toLowerCase().includes(query) || article.title.toLowerCase().includes(query)
    );
    displayArticles(filtered);

    if (!keepTagParam) {
        history.replaceState(null, '', window.location.pathname);
    }
}

loadArticles();
