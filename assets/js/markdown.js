// 記事・解法ページ（details.html?file=…）で .md を表示するための共通処理

function setCanonicalUrl(fileName) {
    const canonical = document.getElementById('canonical-link');
    if (!canonical) return;

    const url = new URL(window.location.href);
    url.search = '';
    url.hash = '';
    url.searchParams.set('file', fileName);
    canonical.href = url.href;
}

// marked が数式中の _ や * を Markdown として解釈しないよう、数式を一旦トークンに置き換える
function protectMarkdownMath(markdown) {
    const codeSegments = [];
    const mathSegments = [];

    const saveCode = (text) => {
        const token = `YURA1685CODETOKEN${codeSegments.length}END`;
        codeSegments.push(text);
        return token;
    };

    const saveMath = (text) => {
        const token = `YURA1685MATHTOKEN${mathSegments.length}END`;
        mathSegments.push(text);
        return token;
    };

    let protectedMarkdown = markdown.replace(/^(```+|~~~+)[^\n]*\n[\s\S]*?^\1[ \t]*$/gm, saveCode);
    protectedMarkdown = protectedMarkdown.replace(/(`+)([^\n]*?)\1/g, saveCode);

    protectedMarkdown = protectedMarkdown.replace(/\$\$[\s\S]*?\$\$/g, saveMath);
    protectedMarkdown = protectedMarkdown.replace(/\\\[[\s\S]*?\\\]/g, saveMath);
    protectedMarkdown = protectedMarkdown.replace(/\\\([\s\S]*?\\\)/g, saveMath);

    protectedMarkdown = protectedMarkdown.replace(
        /(^|[^\\$])(\$(?!\$)(?:\\.|[^\\$\n])+(?<!\\)\$)/gm,
        (match, prefix, math) => prefix + saveMath(math)
    );

    codeSegments.forEach((code, index) => {
        protectedMarkdown = protectedMarkdown.replace(`YURA1685CODETOKEN${index}END`, () => code);
    });

    return { markdown: protectedMarkdown, mathSegments };
}

function restoreMarkdownMath(html, mathSegments) {
    const escapeForHtml = (text) => text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

    mathSegments.forEach((math, index) => {
        html = html.replaceAll(`YURA1685MATHTOKEN${index}END`, () => escapeForHtml(math));
    });
    return html;
}

// Markdown を HTML にして targetDiv に入れる（数式・色付けはまだ）
function renderMarkdown(targetDiv, markdown) {
    const protectedMath = protectMarkdownMath(markdown);
    const html = marked.parse(protectedMath.markdown);
    targetDiv.innerHTML = restoreMarkdownMath(html, protectedMath.mathSegments);

    targetDiv.querySelectorAll('a[href^="http"]').forEach(link => {
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
    });
}

// 数式の表示・コードの色付け・Copy ボタン
async function finishMarkdown(targetDiv) {
    if (window.MathJax && window.MathJax.typesetPromise) {
        await window.MathJax.typesetPromise([targetDiv]);
    }
    if (window.Prism) {
        Prism.highlightAllUnder(targetDiv);
    }
    addCopyButtons(targetDiv);
}
