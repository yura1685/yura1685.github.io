// ライブラリ一覧の検索ボックス。
// 各ライブラリの .md の本文とコードは search.json にまとめてあり、最初に入力したときに読み込む。
// スペース区切りで複数の語を入れると、すべてを含むライブラリだけを表示する。
let librarySearchTexts = null;
let librarySearchLoading = null;

function normalizeSearchText(text) {
    return text.normalize('NFKC').toLowerCase();
}

function decodeHtmlEntities(text) {
    const textarea = document.createElement('textarea');
    textarea.innerHTML = text;
    return textarea.value;
}

function loadLibrarySearchTexts() {
    if (!librarySearchLoading) {
        librarySearchLoading = fetch(new URL('library/search.json', window.location.href))
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(entries => {
                librarySearchTexts = new Map(entries.map(entry => [
                    new URL(entry.url, window.location.href).pathname,
                    normalizeSearchText(decodeHtmlEntities(entry.text)),
                ]));
                filterLibraries();
            })
            .catch(error => console.error('Failed to load library search data.', error));
    }
    return librarySearchLoading;
}

function filterLibraries() {
    const words = normalizeSearchText(document.getElementById('library-search').value)
        .split(/\s+/)
        .filter(word => word);

    if (words.length > 0) loadLibrarySearchTexts();

    let shownTotal = 0;
    document.querySelectorAll('main > section').forEach(section => {
        const items = section.querySelectorAll('.library-item');
        if (items.length === 0) return;

        let shown = 0;
        items.forEach(item => {
            // 検索用データの読み込みが終わるまでは、一覧に出ている名前と説明だけで探す
            const text = librarySearchTexts?.get(new URL(item.href).pathname)
                ?? normalizeSearchText(item.textContent);
            const match = words.every(word => text.includes(word));
            item.hidden = !match;
            if (match) shown++;
        });
        section.hidden = shown === 0;
        shownTotal += shown;
    });

    document.getElementById('library-empty').hidden = shownTotal > 0;
}
