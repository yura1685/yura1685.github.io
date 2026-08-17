const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1999464993&single=true&output=csv";

async function loadBucketList() {
    try {
        const response = await fetch(CSV_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const csvText = await response.text();
        const rows = parseCSV(csvText).slice(1)
            .map(cols => (cols[0] || '').trim())
            .filter(Boolean);
        const tbody = document.getElementById('bucket-list-body');

        for (let i = rows.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [rows[i], rows[j]] = [rows[j], rows[i]];
        }

        rows.forEach((item, index) => {
            const tr = document.createElement('tr');

            const idCell = document.createElement('td');
            idCell.className = 'col-id';
            idCell.textContent = index + 1;

            const itemCell = document.createElement('td');
            itemCell.textContent = item;

            tr.append(idCell, itemCell);
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Failed to load bucket list.', error);
    }
}

loadBucketList();
