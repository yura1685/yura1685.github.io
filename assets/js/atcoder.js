const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1701339970&single=true&output=csv";

// 修正: AtCoderのPerformance / Ratingだけ公式の色区分に合わせる
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

    try {
        const response = await fetch(CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText).slice(1)
            .filter(cols => cols.length >= 5 && !cols.every(value => value.trim() === ''))
            .sort((a, b) => (b[0] || '').trim().localeCompare((a[0] || '').trim()));

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

loadStats();
