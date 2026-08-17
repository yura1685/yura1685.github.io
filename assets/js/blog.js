const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=0&single=true&output=csv";

async function loadData() {
    try {
        const response = await fetch(CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText).slice(1);
        const postsByMonth = {};

        rows.forEach(cols => {
            if (cols.length < 2 || !cols[0]) return;

            const dateStr = cols[0].trim();
            const content = cols[1].trim();
            const month = dateStr.substring(0, 7);

            if (!postsByMonth[month]) postsByMonth[month] = [];
            postsByMonth[month].push({ date: dateStr, content });
        });

        renderInterface(postsByMonth);
    } catch (error) {
        document.getElementById('blog-container').textContent = 'Failed to load log.';
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

        postsByMonth[month].reverse().forEach(post => {
            const postEl = document.createElement('div');
            postEl.className = 'post';

            const date = document.createElement('div');
            date.className = 'post-date';
            date.textContent = post.date;

            const content = document.createElement('div');
            content.className = 'post-content';
            content.textContent = post.content;

            postEl.append(date, content);
            monthDiv.appendChild(postEl);
        });

        blogContainer.appendChild(monthDiv);
    });
}

function switchTab(month, clickedBtn) {
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.month-group').forEach(div => div.classList.remove('active'));
    clickedBtn.classList.add('active');
    document.getElementById(`group-${month}`).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

loadData();
