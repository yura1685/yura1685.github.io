// コードブロックの右上に「Copy」ボタンを付ける
function addCopyButtons(root = document) {
    root.querySelectorAll('pre > code').forEach(code => {
        const pre = code.parentElement;
        if (pre.parentElement.classList.contains('code-block')) return;

        const wrapper = document.createElement('div');
        wrapper.className = 'code-block';
        pre.before(wrapper);
        wrapper.appendChild(pre);

        // コード中の数式を表示した後でも、元のコードをそのままコピーできるようにしておく
        const text = code.textContent;

        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(text);
                button.textContent = 'Copied!';
            } catch (error) {
                button.textContent = 'Failed';
                console.error('Failed to copy code.', error);
            }
            setTimeout(() => { button.textContent = 'Copy'; }, 1500);
        });
        wrapper.appendChild(button);
    });
}

// ライブラリページのように最初から HTML にコードがあるページ用
addCopyButtons();
