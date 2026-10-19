// 公開した Google スプレッドシート（CSV）の読み込みに使う共通処理

// シートごとの CSV の URL
const SHEET_UPDATES_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=0&single=true&output=csv";          // 更新記録（ホーム・ブログ・解法記事一覧）
const SHEET_ARTICLES_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1417312107&single=true&output=csv"; // 記事一覧
const SHEET_ATCODER_RESULTS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRvW2DrRQWYruMIFZxdCcyma3Hp-bDMKP_Y860hJaJWBvdGP2Hli-KnCdABHL-sq30BlcO5CMr8-3x1/pub?gid=1701339970&single=true&output=csv"; // AtCoder の成績

function parseCSV(text) {
    const rows = [];
    let row = [];
    let field = '';
    let inQuotes = false;

    for (let i = 0; i < text.length; i++) {
        const char = text[i];

        if (char === '"') {
            if (inQuotes && text[i + 1] === '"') {
                field += '"';
                i++;
            } else {
                inQuotes = !inQuotes;
            }
        } else if (char === ',' && !inQuotes) {
            row.push(field);
            field = '';
        } else if ((char === '\n' || char === '\r') && !inQuotes) {
            if (char === '\r' && text[i + 1] === '\n') i++;
            row.push(field);
            rows.push(row);
            row = [];
            field = '';
        } else {
            field += char;
        }
    }

    if (field !== '' || row.length > 0) {
        row.push(field);
        rows.push(row);
    }

    return rows;
}

// 1行目の見出し（Date, Title など）から列の番号を探す。大文字・小文字は区別しない
function findColumn(header, ...names) {
    for (const name of names) {
        const index = header.indexOf(name.toLowerCase());
        if (index !== -1) return index;
    }
    return -1;
}

// 記事シートを { date, title, tags, file, desc } の配列にする
function parseArticlesCSV(text) {
    const rows = parseCSV(text);
    if (rows.length === 0) return [];

    const header = rows[0].map(value => value.trim().toLowerCase());
    let columns = {
        date: findColumn(header, 'date'),
        title: findColumn(header, 'title'),
        tags: findColumn(header, 'tags', 'tag'),
        file: findColumn(header, 'file'),
        desc: findColumn(header, 'description', 'desc')
    };
    // 見出しが見つからないときは Date, Title, Tags, File, Description の順とみなす
    if (columns.title === -1 || columns.file === -1) {
        columns = { date: 0, title: 1, tags: 2, file: 3, desc: 4 };
    }

    const get = (cols, index) => (index === -1 ? '' : (cols[index] || '').trim());

    return rows.slice(1).map(cols => ({
        date: get(cols, columns.date),
        title: get(cols, columns.title),
        tags: get(cols, columns.tags).split('|').map(tag => tag.trim()).filter(Boolean),
        file: get(cols, columns.file),
        desc: get(cols, columns.desc)
    })).filter(article => article.title && /^[A-Za-z0-9_-]+\.md$/.test(article.file));
}

// 更新記録の Type と File から、記事・解法ページへのリンクを作る
function buildDetailLink(type, file) {
    if (!file || !/^[A-Za-z0-9_-]+\.md$/.test(file)) return null;

    if (type === 'article') {
        return `/articles/details.html?file=${encodeURIComponent(file)}`;
    }
    if (type === 'atcoder') {
        return `/atcoder/details.html?file=${encodeURIComponent(file)}`;
    }

    return null;
}
