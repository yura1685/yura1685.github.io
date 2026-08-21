const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=0&single=true&output=csv";

function buildPostLink(type, file) {
    if (!file || !/^[A-Za-z0-9_-]+\.md$/.test(file)) return null;

    if (type === 'article') {
        return `../articles/details.html?file=${encodeURIComponent(file)}`;
    }
    if (type === 'atcoder') {
        return `../atcoder/details.html?file=${encodeURIComponent(file)}`;
    }

    return null;
}

async function loadData() {
    try {
        const response = await fetch(CSV_URL);
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

        const postsByMonth = {};

        csv.slice(1).forEach(cols => {
            if (!cols[dateIndex]) return;

            const dateStr = cols[dateIndex].trim();
            const content = (cols[contentIndex] ?? '').trim();
            const type = typeIndex === -1 ? '' : (cols[typeIndex] ?? '').trim().toLowerCase();
            const file = fileIndex === -1 ? '' : (cols[fileIndex] ?? '').trim();
            const link = buildPostLink(type, file);
            const month = dateStr.substring(0, 7);

            if (!postsByMonth[month]) postsByMonth[month] = [];
            postsByMonth[month].push({
                date: dateStr,
                content,
                link
            });
        });

        renderInterface(postsByMonth);
    } catch (error) {
        document.getElementById('blog-container').textContent = 'ブログの読み込みに失敗しました。';
        console.error(error);
    }
}

function renderInterface(postsByMonth) {
    const tabContainer = document.getElementById('tab-container');
    const blogContainer = document.getElementById('blog-container');

    tabContainer.replaceChildren();
    blogContainer.replaceChildren();

    const months = Object.keys(postsByMonth).sort().reverse();

    months.forEach((month, index) => {
        const btn = document.createElement('button');
        btn.className = `tab-button ${index === 0 ? 'active' : ''}`;
        btn.textContent = month;
        btn.onclick = () => switchTab(month, btn);
        tabContainer.appendChild(btn);

        const monthDiv = document.createElement('div');
        monthDiv.id = `group-${month}`;
        monthDiv.className = `month-group ${index === 0 ? 'active' : ''}`;

        postsByMonth[month]
            .sort((a, b) => b.date.localeCompare(a.date))
            .forEach(post => {
                const postEl = document.createElement('div');
                postEl.className = 'post';

                const date = document.createElement('div');
                date.className = 'post-date';
                date.textContent = post.date;

                const content = document.createElement('div');
                content.className = 'post-content';
                content.append(document.createTextNode(post.content));

                if (post.link) {
                    content.append(document.createTextNode(' 詳細は'));

                    const link = document.createElement('a');
                    link.href = post.link;
                    link.textContent = 'こちら';

                    content.append(link);
                }

                postEl.append(date, content);
                monthDiv.appendChild(postEl);
            });

        blogContainer.appendChild(monthDiv);
    });
}

function switchTab(month, clickedBtn) {
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    document.querySelectorAll('.month-group').forEach(div => {
        div.classList.remove('active');
    });

    clickedBtn.classList.add('active');
    document.getElementById(`group-${month}`).classList.add('active');

    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

loadData();
