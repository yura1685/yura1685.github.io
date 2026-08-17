const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1701339970&single=true&output=csv";

async function loadStats() {
    try {
        const response = await fetch(CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText).slice(1);
        const tbody = document.getElementById('stats-body');

        rows.forEach(cols => {
            if (cols.length < 5 || cols.every(value => value.trim() === '')) return;

            const tr = document.createElement('tr');
            for (let i = 0; i < 5; i++) {
                const td = document.createElement('td');
                td.textContent = (cols[i] || '').trim();
                tr.appendChild(td);
            }

            const detailCell = document.createElement('td');
            const fileName = (cols[5] || '').trim();
            if (fileName) {
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
        console.error('Failed to load stats.', error);
    }
}

loadStats();
