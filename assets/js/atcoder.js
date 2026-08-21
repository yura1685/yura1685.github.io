const ATCODER_RESULTS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1701339970&single=true&output=csv";

// 修正: Homeの更新一覧と同じCSVを使い、type=atcoderの記事を独立して取得する
const ATCODER_ARTICLES_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=0&single=true&output=csv";

// AtCoderのPerformance / Ratingだけ公式の色区分に合わせる
function getRatingClass(text) {
    if (!text.trim()) return '';
    const value = Number(text.replace(/,/g, ''));
    if (!Number.isFinite(value)) return '';

    if (value < 400) return 'rating-gray';
    if (value < 800) return 'rating-brown';
    if (value < 1200) return 'rating-green';
    if (value < 1600) return 'rating-cyan';
    if (value < 2000) return 'rating-blue';
    if (value < 2400) return 'rating-yellow';
    if (value < 2800) return 'rating-orange';
    return 'rating-red';
}

async function loadStats() {
    const tbody = document.getElementById('stats-body');
    if (!tbody) return;

    try {
        const response = await fetch(ATCODER_RESULTS_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        let rows = parseCSV(csvText).slice(1)
            .filter(cols => cols.length >= 5 && !cols.every(value => value.trim() === ''))
            .sort((a, b) => (b[0] || '').trim().localeCompare((a[0] || '').trim()));

        // 修正: data-limit があるページだけ表示件数を制限する
        const limit = Number(tbody.dataset.limit || 0);
        if (limit > 0) rows = rows.slice(0, limit);

        tbody.replaceChildren();

        rows.forEach(cols => {
            const tr = document.createElement('tr');
            for (let i = 0; i < 5; i++) {
                const td = document.createElement('td');
                const text = (cols[i] || '').trim();
                td.textContent = text;

                // Performance(3), New Rating(4)のみ色付け
                if (i === 3 || i === 4) {
                    const ratingClass = getRatingClass(text);
                    if (ratingClass) td.classList.add('rating-value', ratingClass);
                }

                tr.appendChild(td);
            }

            const detailCell = document.createElement('td');
            const fileName = (cols[5] || '').trim();
            if (/^[A-Za-z0-9_-]+\.md$/.test(fileName)) {
                const link = document.createElement('a');
                link.href = `details.html?file=${encodeURIComponent(fileName)}`;
                link.className = 'detail-link';
                link.textContent = 'Detail';
                detailCell.appendChild(link);
            }

            tr.appendChild(detailCell);
            tbody.appendChild(tr);
        });
    } catch (error) {
        tbody.replaceChildren();
        const tr = document.createElement('tr');
        const td = document.createElement('td');
        td.colSpan = 6;
        td.textContent = 'AtCoder成績の読み込みに失敗しました。';
        tr.appendChild(td);
        tbody.appendChild(tr);
        console.error('Failed to load stats.', error);
    }
}

function getColumnIndex(header, name) {
    return header.indexOf(name.toLowerCase());
}

function getFallbackSolutionTitle(content, file) {
    if (content) return content;
    return file.replace(/\.md$/i, '').toUpperCase() + ' の解法記事';
}

async function getSolutionTitle(file, fallback) {
    try {
        const response = await fetch(`./solutions/${file}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const markdown = await response.text();
        return markdown.match(/^#\s+(.+)$/m)?.[1]?.trim() || fallback;
    } catch (error) {
        console.warn(`Failed to load title from ${file}.`, error);
        return fallback;
    }
}

async function loadSolutions() {
    const list = document.getElementById('solution-list');
    if (!list) return;

    try {
        const response = await fetch(ATCODER_ARTICLES_CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const csv = parseCSV(csvText);
        if (csv.length === 0) throw new Error('CSV is empty.');

        const header = csv[0].map(value => value.trim().toLowerCase());
        const dateIndex = getColumnIndex(header, 'date');
        const contentIndex = getColumnIndex(header, 'content');
        const typeIndex = getColumnIndex(header, 'type');
        const fileIndex = getColumnIndex(header, 'file');

        if (dateIndex === -1 || typeIndex === -1 || fileIndex === -1) {
            throw new Error('CSV must contain Date, Type and File columns.');
        }

        const solutionMap = new Map();
        csv.slice(1).forEach(cols => {
            const date = (cols[dateIndex] ?? '').trim();
            const type = (cols[typeIndex] ?? '').trim().toLowerCase();
            const file = (cols[fileIndex] ?? '').trim();
            const content = contentIndex === -1 ? '' : (cols[contentIndex] ?? '').trim();

            if (!date || type !== 'atcoder' || !/^[A-Za-z0-9_-]+\.md$/.test(file)) return;

            const current = solutionMap.get(file);
            if (!current || date.localeCompare(current.date) > 0) {
                solutionMap.set(file, { date, file, content });
            }
        });

        let solutions = [...solutionMap.values()].sort((a, b) => b.date.localeCompare(a.date));

        const limit = Number(list.dataset.limit || 0);
        if (limit > 0) solutions = solutions.slice(0, limit);

        solutions = await Promise.all(solutions.map(async solution => ({
            ...solution,
            title: await getSolutionTitle(solution.file, getFallbackSolutionTitle(solution.content, solution.file))
        })));

        renderSolutions(solutions);
    } catch (error) {
        list.replaceChildren();
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.textContent = '解法記事一覧の読み込みに失敗しました。';
        list.appendChild(empty);
        console.error('Failed to load solutions.', error);
    }
}

function renderSolutions(solutions) {
    const list = document.getElementById('solution-list');
    list.replaceChildren();

    if (solutions.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'empty-state';
        empty.textContent = '解法記事はまだありません。';
        list.appendChild(empty);
        return;
    }

    solutions.forEach(solution => {
        const item = document.createElement('a');
        item.className = 'recent-update recent-update-link';
        item.href = `details.html?file=${encodeURIComponent(solution.file)}`;

        const date = document.createElement('time');
        date.className = 'recent-update-date';
        date.textContent = solution.date;

        const title = document.createElement('div');
        title.className = 'recent-update-content';
        title.textContent = solution.title;

        item.append(date, title);
        list.appendChild(item);
    });
}

loadStats();
loadSolutions();
