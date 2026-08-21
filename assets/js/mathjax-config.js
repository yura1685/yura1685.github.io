window.MathJax = {
    tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true
    }
};

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
