const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1999464993&single=true&output=csv";

    async function loadBucketList() {
        try {
            const response = await fetch(CSV_URL);
            const csvText = await response.text();
            let rows = csvText.split('\n').slice(1);
            const tbody = document.getElementById('bucket-list-body');

            for (let i = rows.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [rows[i], rows[j]] = [rows[j], rows[i]];
            }

            rows.forEach((row, index) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td class="col-id">${index + 1}</td>
                    <td>${row}</td>
                `;
                tbody.appendChild(tr);
            });
        } catch (e) {
            console.error("Failed to load bucket list.");
        }
    }
    loadBucketList();
