// 自作問題ページ（problems/index.html）
// ・問題文を Markdown として表示する（数式は MathJax が読み込み時にまとめて表示する）
// ・「すべて / 数学 / プログラミング」で絞り込み、1ページ10問ずつ番号ボタンで切り替える（URL は変わらない）
//   番号ボタンは絞り込みボタンの段の右端と、一覧の下の2か所に出す
// ・問題文が長い箱は途中で切り、下の真ん中の「全て表示」で全文を出す
const PROBLEMS_PER_PAGE = 10;

const problemBoxes = Array.from(document.querySelectorAll('.problem-box'));
const problemList = document.getElementById('problem-list');
const problemPageNavs = document.querySelectorAll('.problem-pages');
const problemToolbar = document.querySelector('.problem-toolbar');
const problemEmpty = document.getElementById('problem-empty');
const problemFilterButtons = document.querySelectorAll('.problem-filter .tab-button');

let problemKind = 'all';
let problemPage = 1;

// 箱の中身が上限の高さを超えているときだけ「全て表示」を出す
// scrollHeight で測ると、数式の文字が行の下へ数px はみ出すだけで「長い」と判定されてしまうので、
// 問題文そのものの高さ（offsetHeight）と、箱の中で見えている高さを比べる
function updateExpandButton(box) {
    if (box.hidden || box.classList.contains('is-open')) return;
    const body = box.querySelector('.problem-body');
    const statement = box.querySelector('.problem-statement');
    const isLong = statement.offsetHeight > body.clientHeight + 1;
    box.classList.toggle('is-long', isLong);
    box.querySelector('.problem-expand').hidden = !isLong;
}

function updateAllExpandButtons() {
    problemBoxes.forEach(updateExpandButton);
}

function renderPageButtons(nav, pageCount) {
    nav.innerHTML = '';
    nav.hidden = pageCount <= 1;
    for (let page = 1; page <= pageCount; page++) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'problem-page-button';
        button.textContent = page;
        if (page === problemPage) {
            button.classList.add('active');
            button.setAttribute('aria-current', 'page');
        }
        button.addEventListener('click', () => {
            if (page === problemPage) return;
            problemPage = page;
            showProblems();
            // 下の番号ボタンで切り替えたときは、一覧の頭（絞り込みボタンの段）まで戻す
            if (nav.classList.contains('problem-pages-bottom')) {
                problemToolbar.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
        nav.appendChild(button);
    }
}

function showProblems() {
    const matched = problemBoxes.filter(box => problemKind === 'all' || box.dataset.kind === problemKind);
    const pageCount = Math.max(1, Math.ceil(matched.length / PROBLEMS_PER_PAGE));
    problemPage = Math.min(problemPage, pageCount);

    const start = (problemPage - 1) * PROBLEMS_PER_PAGE;
    const shown = new Set(matched.slice(start, start + PROBLEMS_PER_PAGE));
    problemBoxes.forEach(box => { box.hidden = !shown.has(box); });

    problemEmpty.hidden = matched.length > 0;
    problemEmpty.textContent = problemBoxes.length === 0
        ? 'まだ問題がありません。'
        : 'この種類の問題はまだありません。';

    problemPageNavs.forEach(nav => renderPageButtons(nav, pageCount));
    updateAllExpandButtons();
}

problemFilterButtons.forEach(button => {
    button.addEventListener('click', () => {
        problemKind = button.dataset.kind;
        problemPage = 1;
        problemFilterButtons.forEach(other => other.classList.toggle('active', other === button));
        showProblems();
    });
});

problemBoxes.forEach(box => {
    const statement = box.querySelector('.problem-statement');
    renderMarkdown(statement, statement.textContent);

    const button = box.querySelector('.problem-expand');
    button.addEventListener('click', () => {
        const isOpen = box.classList.toggle('is-open');
        button.textContent = isOpen ? '閉じる' : '全て表示';
        // 閉じたときに箱の上端が画面の外なら、箱の頭まで戻す
        if (!isOpen && box.getBoundingClientRect().top < 0) {
            box.scrollIntoView({ block: 'start' });
        }
    });
});

showProblems();

// 数式が表示されると高さが変わるので、MathJax の処理が終わってからもう一度測る
window.addEventListener('load', async () => {
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        await window.MathJax.startup.promise;
    }
    updateAllExpandButtons();
});
window.addEventListener('resize', updateAllExpandButtons);
