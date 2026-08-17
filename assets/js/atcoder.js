const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1701339970&single=true&output=csv";

    async function loadStats() {
        try {
            const response = await fetch(CSV_URL);
            const csvText = await response.text();
            const rows = csvText.split('\n').slice(1);
            const tbody = document.getElementById('stats-body');

            rows.forEach(row => {
                const cols = row.split(',');
                const fileName = (cols[5] && cols[5].trim() !== "") ? cols[5].trim() : null;
                const detailButton = fileName 
                    ? `<a href="details.html?file=${fileName}" class="detail-link">Detail</a>` 
                    : "";

                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${cols[0]}</td>
                    <td>${cols[1]}</td>
                    <td>${cols[2]}</td>
                    <td>${cols[3]}</td>
                    <td>${cols[4]}</td>
                    <td>${detailButton}</td>
                `;
                tbody.appendChild(tr);
            });
        } catch (e) {
            console.error("Failed to load stats.");
        }
    }
    loadStats();
