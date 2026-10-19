// Playground（playground/index.html）: 左に書いた Markdown を右に表示し、ブラウザに保存する

const DOCS_KEY = 'playground-docs';       // 保存したもの [{ id, title, text, savedAt }]
const DRAFT_KEY = 'playground-draft';     // 書きかけ（再読み込みしても消えないように）
const SPLIT_KEY = 'playground-split';     // 左側の幅（%）
const VIEW_KEY = 'playground-view';       // 表示（edit / split / preview）
const SIDEBAR_KEY = 'playground-sidebar'; // 左の一覧をたたんでいるか

const app = document.getElementById('pg-app');
const workspace = document.getElementById('pg-workspace');
const divider = document.getElementById('pg-divider');
const preview = document.getElementById('pg-preview');
const titleInput = document.getElementById('pg-title');
const docList = document.getElementById('pg-doc-list');
const docTemplate = document.getElementById('pg-doc-template');
const sidebarToggle = document.getElementById('pg-sidebar-toggle');
const statusElement = document.getElementById('pg-status');
const countElement = document.getElementById('pg-count');
const narrowScreen = window.matchMedia('(max-width: 700px)');

const sampleText = document.getElementById('pg-editor').value;
let currentId = null; // 今開いている（保存済みの）ものの id

// localStorage が使えないブラウザ設定でも止まらないようにする
function readStorage(key, fallback) {
    try {
        const value = localStorage.getItem(key);
        return value === null ? fallback : JSON.parse(value);
    } catch (error) {
        return fallback;
    }
}

function writeStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Failed to write to localStorage.', error);
        return false;
    }
}

// 前の版（name で管理していたもの）も読めるように、id と title をそろえて返す
function readDocs() {
    const docs = readStorage(DOCS_KEY, []);
    if (!Array.isArray(docs)) return [];
    return docs.map((doc, index) => ({
        id: doc.id || `old-${index}-${doc.savedAt || ''}`,
        title: doc.title ?? doc.name ?? '無題',
        text: doc.text ?? '',
        savedAt: doc.savedAt || ''
    }));
}

function findDoc(id) {
    return id ? readDocs().find(doc => doc.id === id) || null : null;
}

function makeId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

// --- エディタ ---

const cm = CodeMirror.fromTextArea(document.getElementById('pg-editor'), {
    mode: {
        name: 'markdown',
        // ``` の中身や `code` は記事ページと同じ色にするため、名前を変えておく
        tokenTypeOverrides: { code: 'md-code', list1: 'md-list', list2: 'md-list', list3: 'md-list', linkHref: 'md-url' }
    },
    lineNumbers: true,
    lineWrapping: true,
    styleActiveLine: true,
    foldGutter: true,
    gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
    indentUnit: 4,
    placeholder: 'ここに Markdown を書きます',
    extraKeys: {
        'Ctrl-S': saveDoc,
        'Cmd-S': saveDoc,
        'Ctrl-B': () => runTool('bold'),
        'Cmd-B': () => runTool('bold'),
        Tab: editor => editor.execCommand(editor.somethingSelected() ? 'indentMore' : 'insertSoftTab'),
        'Shift-Tab': 'indentLess'
    }
});

function hasUnsavedChanges() {
    const saved = findDoc(currentId);
    if (saved) return saved.text !== cm.getValue() || saved.title !== titleInput.value.trim();
    const text = cm.getValue();
    return text.trim() !== '' && text !== sampleText;
}

function showStatus(message, state = '') {
    statusElement.textContent = message;
    statusElement.dataset.state = state;
}

function updateStatus() {
    if (hasUnsavedChanges()) {
        showStatus('未保存の変更があります', 'unsaved');
    } else if (findDoc(currentId)) {
        showStatus('保存済み', 'saved');
    } else {
        showStatus('');
    }
}

function saveDraft() {
    writeStorage(DRAFT_KEY, { title: titleInput.value, text: cm.getValue(), currentId });
}

// --- 入力補助ボタン ---

// 選んでいる文字を before と after で挟む（何も選んでいなければ見本の文字を入れて選んだ状態にする）
function wrapSelection(before, after, placeholder) {
    const text = cm.getSelection() || placeholder;
    cm.replaceSelection(before + text + after);
    const end = cm.indexFromPos(cm.getCursor()) - after.length;
    cm.setSelection(cm.posFromIndex(end - text.length), cm.posFromIndex(end));
}

// コードや $$ の数式のように、行の頭から始めるもの
function insertBlock(before, after, placeholder) {
    const lineBreak = cm.getCursor('from').ch === 0 ? '' : '\n';
    wrapSelection(lineBreak + before, after, placeholder);
}

// 今の行を見出し（##）にする。もう見出しなら元に戻す
function toggleHeading() {
    const line = cm.getCursor().line;
    const marks = cm.getLine(line).match(/^#{1,6}\s+/);
    if (marks) {
        cm.replaceRange('', { line, ch: 0 }, { line, ch: marks[0].length });
    } else {
        cm.replaceRange('## ', { line, ch: 0 });
    }
}

const tools = {
    heading: toggleHeading,
    bold: () => wrapSelection('**', '**', '太字'),
    code: () => wrapSelection('`', '`', 'code'),
    math: () => wrapSelection('$', '$', 'x^2'),
    displayMath: () => insertBlock('$$\n', '\n$$', '\\sum_{k=1}^{n} k'),
    codeBlock: () => insertBlock('```python\n', '\n```', 'print("Hello")'),
    table: () => insertBlock('| 見出し | 見出し |\n| --- | --- |\n| ', ' | セル |', 'セル'),
    link: () => wrapSelection('[', '](https://)', 'リンクの文字'),
    image: () => wrapSelection('![', '](画像のURL)', '説明')
};

function runTool(name) {
    tools[name]();
    cm.focus();
}

document.querySelectorAll('.pg-tool').forEach(button => {
    button.addEventListener('click', () => runTool(button.dataset.action));
});

// --- プレビュー ---

let isRendering = false;
let needsRender = false;
let previewIsStale = false;

// 右を左と同じ割合までスクロールする（左がスクロールできないときは何もしない）
function syncPreviewScroll() {
    const info = cm.getScrollInfo();
    const editorRange = info.height - info.clientHeight;
    if (editorRange <= 0) return false;
    preview.scrollTop = info.top / editorRange * (preview.scrollHeight - preview.clientHeight);
    return true;
}

async function updatePreview() {
    // エディタだけの表示中は、プレビューに戻ったときに表示する
    if (app.dataset.view === 'edit') {
        previewIsStale = true;
        return;
    }
    if (isRendering) {
        needsRender = true;
        return;
    }
    isRendering = true;
    previewIsStale = false;

    const scrollTop = preview.scrollTop;
    try {
        // 前回の数式を MathJax の管理から外す（入力のたびに溜まらないように）
        if (window.MathJax && window.MathJax.typesetClear) {
            MathJax.typesetClear([preview]);
        }
        renderMarkdown(preview, cm.getValue());
        await finishMarkdown(preview);
    } catch (error) {
        console.error('Failed to render the preview.', error);
    }
    if (!syncPreviewScroll()) preview.scrollTop = scrollTop;

    isRendering = false;
    if (needsRender) {
        needsRender = false;
        updatePreview();
    }
}

let editTimer = null;

cm.on('change', () => {
    countElement.textContent = `${cm.getValue().length.toLocaleString()} 文字`;
    clearTimeout(editTimer);
    editTimer = setTimeout(() => {
        updatePreview();
        saveDraft();
        updateStatus();
    }, 200);
});

cm.on('scroll', syncPreviewScroll);

// --- 保存・開く・削除 ---

function formatDate(isoString) {
    const date = new Date(isoString);
    if (Number.isNaN(date.getTime())) return '';
    return date.toLocaleString('ja-JP', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function renderDocList() {
    const docs = readDocs().sort((a, b) => b.savedAt.localeCompare(a.savedAt));
    docList.replaceChildren();

    if (docs.length === 0) {
        const empty = document.createElement('li');
        empty.className = 'pg-doc-empty';
        empty.textContent = 'まだありません';
        docList.appendChild(empty);
        return;
    }

    docs.forEach(doc => {
        const item = docTemplate.content.firstElementChild.cloneNode(true);
        item.classList.toggle('active', doc.id === currentId);
        item.querySelector('.pg-doc-title').textContent = doc.title;
        item.querySelector('.pg-doc-date').textContent = formatDate(doc.savedAt);
        item.querySelector('.pg-doc-open').addEventListener('click', () => openSavedDoc(doc.id));

        const deleteButton = item.querySelector('.pg-doc-delete');
        deleteButton.setAttribute('aria-label', `「${doc.title}」を削除`);
        deleteButton.addEventListener('click', () => deleteDoc(doc.id));

        docList.appendChild(item);
    });
}

// 保存したもの（doc）か、まっさら（null）をエディタに出す
function openDoc(doc) {
    currentId = doc ? doc.id : null;
    titleInput.value = doc ? doc.title : '';
    cm.setValue(doc ? doc.text : '');
    cm.clearHistory();
    saveDraft();
    renderDocList();
    updateStatus();
}

function openSavedDoc(id) {
    const doc = findDoc(id);
    if (!doc || id === currentId) return;
    if (hasUnsavedChanges() && !confirm('保存していない変更は消えます。開きますか？')) return;
    openDoc(doc);
    if (narrowScreen.matches) setSidebarCollapsed(true);
}

function saveDoc() {
    const docs = readDocs();
    const doc = {
        id: currentId || makeId(),
        title: titleInput.value.trim() || '無題',
        text: cm.getValue(),
        savedAt: new Date().toISOString()
    };
    const index = docs.findIndex(item => item.id === doc.id);
    if (index === -1) {
        docs.push(doc);
    } else {
        docs[index] = doc;
    }

    if (!writeStorage(DOCS_KEY, docs)) {
        showStatus('保存できませんでした', 'error');
        return;
    }

    currentId = doc.id;
    titleInput.value = doc.title;
    saveDraft();
    renderDocList();
    updateStatus();
}

function deleteDoc(id) {
    const doc = findDoc(id);
    if (!doc || !confirm(`「${doc.title}」を削除しますか？（元に戻せません）`)) return;

    writeStorage(DOCS_KEY, readDocs().filter(item => item.id !== id));
    if (id === currentId) currentId = null;
    saveDraft();
    renderDocList();
    updateStatus();
}

document.getElementById('pg-save').addEventListener('click', saveDoc);

document.getElementById('pg-new').addEventListener('click', () => {
    if (hasUnsavedChanges() && !confirm('保存していない変更は消えます。新しく書き始めますか？')) return;
    openDoc(null);
    cm.focus();
});

titleInput.addEventListener('input', () => {
    saveDraft();
    updateStatus();
});

titleInput.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.isComposing) {
        event.preventDefault();
        saveDoc();
    }
});

// エディタの外にいるときの Ctrl+S（Mac は ⌘+S）
document.addEventListener('keydown', event => {
    if (event.defaultPrevented) return;
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
        event.preventDefault();
        saveDoc();
    }
});

// 別のタブで保存・削除したときも一覧を合わせる
window.addEventListener('storage', event => {
    if (event.key === DOCS_KEY) {
        renderDocList();
        updateStatus();
    }
});

// --- 表示の切り替え・左の一覧 ---

function setView(view) {
    app.dataset.view = view;
    document.querySelectorAll('.pg-view-button').forEach(button => {
        button.setAttribute('aria-pressed', button.dataset.viewButton === view);
    });
    cm.refresh();
    if (view !== 'edit' && previewIsStale) updatePreview();
}

document.querySelectorAll('.pg-view-button').forEach(button => {
    button.addEventListener('click', () => {
        setView(button.dataset.viewButton);
        writeStorage(VIEW_KEY, button.dataset.viewButton);
    });
});

function setSidebarCollapsed(collapsed) {
    app.classList.toggle('pg-sidebar-collapsed', collapsed);
    const label = collapsed ? '一覧を開く' : '一覧をたたむ';
    sidebarToggle.title = label;
    sidebarToggle.setAttribute('aria-label', label);
    sidebarToggle.setAttribute('aria-expanded', !collapsed);
    cm.refresh();
}

sidebarToggle.addEventListener('click', () => {
    const collapsed = !app.classList.contains('pg-sidebar-collapsed');
    setSidebarCollapsed(collapsed);
    writeStorage(SIDEBAR_KEY, collapsed);
});

// スマホで一覧を開いているときは、ほかの場所を触ると閉じる
workspace.addEventListener('pointerdown', () => {
    if (narrowScreen.matches && !app.classList.contains('pg-sidebar-collapsed')) setSidebarCollapsed(true);
});

// --- 左右の幅 ---

function setSplit(percent) {
    const value = Math.min(80, Math.max(20, percent));
    workspace.style.setProperty('--pg-split', `${value}%`);
    divider.setAttribute('aria-valuenow', Math.round(value));
    return value;
}

let split = setSplit(Number(readStorage(SPLIT_KEY, 50)) || 50);
let refreshFrame = null;

function saveSplit() {
    writeStorage(SPLIT_KEY, split);
    cm.refresh();
}

divider.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    event.preventDefault();
    divider.setPointerCapture(event.pointerId);
    document.body.classList.add('pg-resizing');
});

divider.addEventListener('pointermove', event => {
    if (!divider.hasPointerCapture(event.pointerId)) return;
    const rect = workspace.getBoundingClientRect();
    split = setSplit((event.clientX - rect.left - divider.offsetWidth / 2) / rect.width * 100);
    // エディタの折り返し位置を測り直す（動かしている間は1フレームに1回だけ）
    if (!refreshFrame) {
        refreshFrame = requestAnimationFrame(() => {
            refreshFrame = null;
            cm.refresh();
        });
    }
});

divider.addEventListener('lostpointercapture', () => {
    document.body.classList.remove('pg-resizing');
    saveSplit();
});

// ダブルクリックで半分ずつに戻す
divider.addEventListener('dblclick', () => {
    split = setSplit(50);
    saveSplit();
});

divider.addEventListener('keydown', event => {
    const step = { ArrowLeft: -2, ArrowRight: 2 }[event.key];
    if (!step) return;
    event.preventDefault();
    split = setSplit(split + step);
    saveSplit();
});

// --- 最初の表示 ---

// 前の版のデータに id を付けて保存し直す
const storedDocs = readStorage(DOCS_KEY, []);
if (Array.isArray(storedDocs) && storedDocs.some(doc => !doc.id)) {
    writeStorage(DOCS_KEY, readDocs());
}

const draft = readStorage(DRAFT_KEY, null);
if (draft && typeof draft.text === 'string') {
    titleInput.value = draft.title ?? draft.name ?? '';
    currentId = draft.currentId || readDocs().find(doc => doc.title === draft.currentName)?.id || null;
    cm.setValue(draft.text);
    cm.clearHistory();
}

countElement.textContent = `${cm.getValue().length.toLocaleString()} 文字`;
// スマホでは一覧をたたんだ状態から始める
setSidebarCollapsed(narrowScreen.matches || readStorage(SIDEBAR_KEY, false) === true);

const savedView = readStorage(VIEW_KEY, 'split');
setView(['edit', 'split', 'preview'].includes(savedView) ? savedView : 'split');
renderDocList();
updateStatus();
updatePreview();

// MathJax は後から読み込まれるので、準備ができたらもう一度表示する
document.addEventListener('DOMContentLoaded', () => {
    if (window.MathJax && window.MathJax.startup) {
        MathJax.startup.promise.then(updatePreview);
    }
});
