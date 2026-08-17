const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1417312107&single=true&output=csv";
let allArticles = [];

function normalizeArticleFileName(fileName) {
    const name = fileName.trim();
    return name.endsWith('.tex') ? `${name.slice(0, -4)}.html` : name;
}

async function loadArticles() {
    try {
        const response = await fetch(CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText).slice(1).reverse();

        allArticles = rows.map(cols => {
            if (cols.length < 4 || !cols[0] || !cols[1] || !cols[3]) return null;
            return {
                date: cols[0].trim(),
                title: cols[1].trim(),
                tags: (cols[2] || '').trim(),
                file: normalizeArticleFileName(cols[3]),
                desc: (cols[4] || '').trim()
            };
        }).filter(Boolean);

        displayArticles(allArticles);
    } catch (error) {
        console.error('Failed to load articles.', error);
    }
}

function displayArticles(articles) {
    const list = document.getElementById('article-list');
    list.replaceChildren();

    articles.forEach(article => {
        const card = document.createElement('a');
        card.className = 'article-card';
        card.href = `details.html?file=${encodeURIComponent(article.file)}&title=${encodeURIComponent(article.title)}`;

        const date = document.createElement('div');
        date.className = 'article-date';
        date.textContent = article.date;

        const title = document.createElement('div');
        title.className = 'article-title';
        title.textContent = article.title;

        const desc = document.createElement('p');
        desc.className = 'article-desc';
        desc.textContent = article.desc;

        const tags = document.createElement('div');
        tags.className = 'article-tags';
        article.tags.split('|').map(tag => tag.trim()).filter(Boolean).forEach(tag => {
            const badge = document.createElement('span');
            badge.className = 'tag-badge';
            badge.textContent = tag;
            tags.appendChild(badge);
        });

        card.append(date, title, desc, tags);
        list.appendChild(card);
    });
}

function filterArticles() {
    const query = document.getElementById('tag-filter').value.toLowerCase();
    const filtered = allArticles.filter(article =>
        article.tags.toLowerCase().includes(query) || article.title.toLowerCase().includes(query)
    );
    displayArticles(filtered);
}

loadArticles();
