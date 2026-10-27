// コードブロックの中の $…$ を数式として表示する
// ・Python（```python）: コメント（# …）と """…""" の中だけ
// ・言語指定なし（```）: ブロック全体
// （MathJax は普段 <pre>・<code> の中を数式にしないので、色付けの後でその部分だけ数式にする）
async function typesetCodeMath(root = document) {
    if (!window.MathJax || !window.MathJax.startup) return;
    await MathJax.startup.promise;

    let parts = [...root.querySelectorAll(
        'pre > code.language-python .token.comment, pre > code.language-python .token.triple-quoted-string'
    )];

    // 言語指定なしのブロックは中身を <span> で包んで渡す（<code> をそのまま渡すと MathJax が飛ばすため）
    root.querySelectorAll('pre > code:not([class*="language-"])').forEach(code => {
        if (code.querySelector(':scope > .code-math')) return;
        const span = document.createElement('span');
        span.className = 'code-math';
        span.append(...code.childNodes);
        code.appendChild(span);
        parts.push(span);
    });

    parts = parts.filter(part => part.textContent.includes('$'));
    if (parts.length > 0) {
        await MathJax.typesetPromise(parts);
    }
}

// ライブラリページのように最初から HTML にコードがあるページ用（色付けが終わった後に行う）
window.addEventListener('load', () => typesetCodeMath());
