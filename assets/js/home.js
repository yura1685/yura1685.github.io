// 修正: Blog用スプレッドシートからHomeに最新5件を表示
const HOME_BLOG_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=0&single=true&output=csv";
const RECENT_UPDATE_LIMIT = 5;

function buildRecentUpdateLink(type, file) {
    if (!file || !/^[A-Za-z0-9_-]+\.md$/.test(file)) return null;

    if (type === 'article') {
        return `articles/details.html?file=${encodeURIComponent(file)}`;
    }
    if (type === 'atcoder') {
        return `atcoder/details.html?file=${encodeURIComponent(file)}`;
    }

    return null;
}

async function loadRecentUpdates() {
    const list = document.getElementById('recent-updates-list');

    try {
        const response = await fetch(HOME_BLOG_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const csv = parseCSV(csvText);
        if (csv.length === 0) throw new Error('CSV is empty.');

        const header = csv[0].map(value => value.trim().toLowerCase());
        const dateIndex = header.indexOf('date');
        const contentIndex = header.indexOf('content');
        const typeIndex = header.indexOf('type');
        const fileIndex = header.indexOf('file');

        if (dateIndex === -1 || contentIndex === -1) {
            throw new Error('CSV must contain Date and Content columns.');
        }

        const updates = csv.slice(1).map(cols => {
            const date = (cols[dateIndex] ?? '').trim();
            if (!date) return null;

            const content = (cols[contentIndex] ?? '').trim();
            const type = typeIndex === -1 ? '' : (cols[typeIndex] ?? '').trim().toLowerCase();
            const file = fileIndex === -1 ? '' : (cols[fileIndex] ?? '').trim();

            return {
                date,
                content,
                link: buildRecentUpdateLink(type, file)
            };
        }).filter(Boolean)
            .sort((a, b) => b.date.localeCompare(a.date))
            .slice(0, RECENT_UPDATE_LIMIT);

        renderRecentUpdates(updates);
    } catch (error) {
        list.textContent = '最近の更新の読み込みに失敗しました。';
        list.classList.add('empty-state');
        console.error('Failed to load recent updates.', error);
    }
}

function renderRecentUpdates(updates) {
    const list = document.getElementById('recent-updates-list');
    list.replaceChildren();

    if (updates.length === 0) {
        list.textContent = '更新はまだありません。';
        list.classList.add('empty-state');
        return;
    }

    updates.forEach(update => {
        const item = document.createElement(update.link ? 'a' : 'div');
        item.className = `recent-update${update.link ? ' recent-update-link' : ''}`;
        if (update.link) item.href = update.link;

        const date = document.createElement('time');
        date.className = 'recent-update-date';
        date.textContent = update.date;

        const content = document.createElement('div');
        content.className = 'recent-update-content';
        content.textContent = update.content;

        item.append(date, content);
        list.appendChild(item);
    });
}

loadRecentUpdates();
