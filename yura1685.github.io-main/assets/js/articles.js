const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1417312107&single=true&output=csv";
    let allArticles = [];

    async function loadArticles() {
        try {
            const response = await fetch(CSV_URL);
            const csvText = await response.text();
            const rows = csvText.split('\n').slice(1).reverse();
            
            allArticles = rows.map(row => {
                const cols = row.split(',');
                if (cols.length < 4) return null;
                return { date: cols[0], title: cols[1], tags: cols[2], file: cols[3], desc: cols[4] || "" };
            }).filter(a => a);

            displayArticles(allArticles);
        } catch (e) { console.error(e); }
    }

    function displayArticles(articles) {
        const list = document.getElementById('article-list');
        list.innerHTML = "";
        articles.forEach(article => {
            const tagsHtml = article.tags.split('|').map(t => `<span class="tag-badge">${t.trim()}</span>`).join('');
            const card = document.createElement('a');
            card.className = 'article-card';
            const encodedTitle = encodeURIComponent(article.title);
            card.href = `details.html?file=${article.file}&title=${encodedTitle}`;
            card.innerHTML = `
                <div class="article-date">${article.date}</div>
                <div class="article-title">${article.title}</div>
                <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 10px;">${article.desc}</p>
                <div class="article-tags">${tagsHtml}</div>
            `;
            list.appendChild(card);
        });
    }

    function filterArticles() {
        const query = document.getElementById('tag-filter').value.toLowerCase();
        const filtered = allArticles.filter(a => a.tags.toLowerCase().includes(query) || a.title.toLowerCase().includes(query));
        displayArticles(filtered);
    }

    loadArticles();
