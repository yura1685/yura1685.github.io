const params = new URLSearchParams(window.location.search);
    const fileName = params.get('file');

    async function loadArticle() {
        const targetDiv = document.getElementById('tex-content');
        if (!fileName) {
            targetDiv.innerText = "ファイルが指定されていません。";
            return;
        }

        try {
            // 解説用texは atcoder/solutions/ 内に配置
            const response = await fetch(`./solutions/${fileName}`);
            if (!response.ok) throw new Error("Not found");
            const text = await response.text();

            targetDiv.innerHTML = text;

            // コードブロックのトリミング (アップロードされたファイルの設定を反映)
            targetDiv.querySelectorAll('pre code').forEach(codeBlock => {
                codeBlock.textContent = codeBlock.textContent.trim();
            });

            // レンダリング実行
            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([targetDiv]);
            }
            if (window.Prism) {
                Prism.highlightAllUnder(targetDiv);
            }
        } catch (e) {
            targetDiv.innerHTML = "記事の読み込みに失敗しました。";
        }
    }
    loadArticle();
