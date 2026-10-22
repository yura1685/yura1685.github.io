// Python のコードブロックで、コメント（# …）と """…""" の中の $…$ を数式として表示する
// （MathJax は普段 <pre>・<code> の中を数式にしないので、色付けの後でその部分だけ数式にする）
async function typesetCodeMath(root = document) {
    if (!window.MathJax || !window.MathJax.startup) return;
    await MathJax.startup.promise;

    const parts = [...root.querySelectorAll(
        'pre > code.language-python .token.comment, pre > code.language-python .token.triple-quoted-string'
    )].filter(part => part.textContent.includes('$'));
    if (parts.length > 0) {
        await MathJax.typesetPromise(parts);
    }
}

// ライブラリページのように最初から HTML にコードがあるページ用（色付けが終わった後に行う）
window.addEventListener('load', () => typesetCodeMath());
