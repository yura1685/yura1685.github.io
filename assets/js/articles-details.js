const params = new URLSearchParams(window.location.search);
    const fileName = params.get('file');
    const pageTitle = params.get('title');

    async function loadArticle() {
        const targetDiv = document.getElementById('tex-content');
        const titleElement = document.getElementById('display-title');

        if (pageTitle) {
            titleElement.innerText = pageTitle;
            document.title = `${pageTitle} | yura1685`;
        }

        if (!fileName) {
            targetDiv.innerText = "ファイルが指定されていません。";
            return;
        }

        try {
            const response = await fetch(`./contents/${fileName}`); // 記事用texの保存先: articles/contents/
            if (!response.ok) throw new Error("Not found");
            const text = await response.text();

            targetDiv.innerHTML = text;

            targetDiv.querySelectorAll('pre code').forEach(codeBlock => {
                codeBlock.textContent = codeBlock.textContent.trim();
            });
            // 各種レンダリング実行
            if (window.MathJax && window.MathJax.typesetPromise) {
                window.MathJax.typesetPromise([targetDiv]);
            }
            if (window.Prism) {
                Prism.highlightAllUnder(targetDiv);
            }
        } catch (e) {
            targetDiv.innerHTML = "Error loading article.";
        }
    }
    loadArticle();
