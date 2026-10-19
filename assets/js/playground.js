// Playground（playground/index.html）: 左に書いた Markdown を右に表示し、名前をつけてブラウザに保存する

const DOCS_KEY = 'playground-docs';   // 保存したもの [{ name, text, savedAt }]
const DRAFT_KEY = 'playground-draft'; // 書きかけ（再読み込みしても消えないように）
const SPLIT_KEY = 'playground-split'; // 左側の幅（%）

const playground = document.getElementById('playground');
const editor = document.getElementById('playground-editor');
const divider = document.getElementById('playground-divider');
const preview = document.getElementById('playground-preview');
const nameInput = document.getElementById('playground-name');
const docSelect = document.getElementById('playground-docs');
const statusElement = document.getElementById('playground-status');

const sampleText = editor.defaultValue;
let currentName = ''; // 今開いている（保存済みの）ものの名前

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

function readDocs() {
    const docs = readStorage(DOCS_KEY, []);
    return Array.isArray(docs) ? docs : [];
}

function findDoc(name) {
    return readDocs().find(doc => doc.name === name) || null;
}

function showStatus(message) {
    statusElement.textContent = message;
}

function hasUnsavedChanges() {
    const saved = currentName ? findDoc(currentName) : null;
    if (saved) return saved.text !== editor.value;
    return editor.value.trim() !== '' && editor.value !== sampleText;
}

function saveDraft() {
    writeStorage(DRAFT_KEY, { name: nameInput.value, text: editor.value, currentName });
}

// --- 表示 ---

// 右を左と同じ割合までスクロールする（左がスクロールできないときは何もしない）
function syncPreviewScroll() {
    const editorRange = editor.scrollHeight - editor.clientHeight;
    if (editorRange <= 0) return false;
    preview.scrollTop = editor.scrollTop / editorRange * (preview.scrollHeight - preview.clientHeight);
    return true;
}

let isRendering = false;
let needsRender = false;

async function updatePreview() {
    if (isRendering) {
        needsRender = true;
        return;
    }
    isRendering = true;

    const scrollTop = preview.scrollTop;
    try {
        // 前回の数式を MathJax の管理から外す（入力のたびに溜まらないように）
        if (window.MathJax && window.MathJax.typesetClear) {
            MathJax.typesetClear([preview]);
        }
        renderMarkdown(preview, editor.value);
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

editor.addEventListener('input', () => {
    clearTimeout(editTimer);
    editTimer = setTimeout(() => {
        updatePreview();
        saveDraft();
        showStatus(hasUnsavedChanges() ? '未保存の変更があります' : '');
    }, 200);
});

editor.addEventListener('scroll', syncPreviewScroll);

// Tab キーで字下げする（execCommand なら Ctrl+Z で戻せる）
editor.addEventListener('keydown', event => {
    if (event.key !== 'Tab' || event.shiftKey || event.ctrlKey || event.altKey || event.metaKey || event.isComposing) return;
    event.preventDefault();
    if (!document.execCommand('insertText', false, '    ')) {
        editor.setRangeText('    ', editor.selectionStart, editor.selectionEnd, 'end');
        editor.dispatchEvent(new Event('input'));
    }
});

// --- 保存・開く・削除 ---

function refreshDocList() {
    const docs = readDocs().sort((a, b) => (b.savedAt || '').localeCompare(a.savedAt || ''));

    docSelect.replaceChildren(new Option(docs.length ? '保存したものを開く…' : '保存したものはまだありません', ''));
    docs.forEach(doc => docSelect.add(new Option(doc.name, doc.name)));
    docSelect.value = docs.some(doc => doc.name === currentName) ? currentName : '';
}

function openDoc(name, text) {
    currentName = name;
    nameInput.value = name;
    editor.value = text;
    editor.scrollTop = 0;
    preview.scrollTop = 0;
    saveDraft();
    refreshDocList();
    updatePreview();
}

function saveDoc() {
    const name = nameInput.value.trim();
    if (!name) {
        showStatus('名前を入れてください');
        nameInput.focus();
        return;
    }

    const docs = readDocs();
    const index = docs.findIndex(doc => doc.name === name);
    if (index !== -1 && name !== currentName && !confirm(`「${name}」はもう保存されています。上書きしますか？`)) {
        return;
    }

    const doc = { name, text: editor.value, savedAt: new Date().toISOString() };
    if (index === -1) {
        docs.push(doc);
    } else {
        docs[index] = doc;
    }

    if (!writeStorage(DOCS_KEY, docs)) {
        showStatus('保存できませんでした');
        return;
    }

    currentName = name;
    nameInput.value = name;
    saveDraft();
    refreshDocList();
    showStatus(`保存しました（${new Date().toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' })}）`);
}

document.getElementById('playground-save').addEventListener('click', saveDoc);

nameInput.addEventListener('input', saveDraft);
nameInput.addEventListener('keydown', event => {
    if (event.key === 'Enter' && !event.isComposing) {
        event.preventDefault();
        saveDoc();
    }
});

// Ctrl+S（Mac は ⌘+S）で保存する
document.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
        event.preventDefault();
        saveDoc();
    }
});

docSelect.addEventListener('change', () => {
    const doc = findDoc(docSelect.value);
    if (!doc || (hasUnsavedChanges() && !confirm('保存していない変更は消えます。開きますか？'))) {
        refreshDocList();
        return;
    }
    openDoc(doc.name, doc.text);
    showStatus(`「${doc.name}」を開きました`);
});

document.getElementById('playground-delete').addEventListener('click', () => {
    const name = docSelect.value;
    if (!name) {
        showStatus('削除するものを選んでください');
        return;
    }
    if (!confirm(`「${name}」を削除しますか？（元に戻せません）`)) return;

    writeStorage(DOCS_KEY, readDocs().filter(doc => doc.name !== name));
    if (name === currentName) currentName = '';
    saveDraft();
    refreshDocList();
    showStatus(`「${name}」を削除しました`);
});

document.getElementById('playground-new').addEventListener('click', () => {
    if (hasUnsavedChanges() && !confirm('保存していない変更は消えます。新しく書き始めますか？')) return;
    openDoc('', '');
    showStatus('');
    editor.focus();
});

// 別のタブで保存・削除したときも一覧を合わせる
window.addEventListener('storage', event => {
    if (event.key === DOCS_KEY) refreshDocList();
});

// --- 左右の幅 ---

function setSplit(percent) {
    const value = Math.min(80, Math.max(20, percent));
    playground.style.setProperty('--playground-split', `${value}%`);
    divider.setAttribute('aria-valuenow', Math.round(value));
    return value;
}

let split = setSplit(Number(readStorage(SPLIT_KEY, 50)) || 50);

divider.addEventListener('pointerdown', event => {
    if (event.button !== 0) return;
    event.preventDefault();
    divider.setPointerCapture(event.pointerId);
    document.body.classList.add('playground-resizing');
});

divider.addEventListener('pointermove', event => {
    if (!divider.hasPointerCapture(event.pointerId)) return;
    const rect = playground.getBoundingClientRect();
    split = setSplit((event.clientX - rect.left - divider.offsetWidth / 2) / rect.width * 100);
});

divider.addEventListener('lostpointercapture', () => {
    document.body.classList.remove('playground-resizing');
    writeStorage(SPLIT_KEY, split);
});

// ダブルクリックで半分ずつに戻す
divider.addEventListener('dblclick', () => {
    split = setSplit(50);
    writeStorage(SPLIT_KEY, split);
});

divider.addEventListener('keydown', event => {
    const step = { ArrowLeft: -2, ArrowRight: 2 }[event.key];
    if (!step) return;
    event.preventDefault();
    split = setSplit(split + step);
    writeStorage(SPLIT_KEY, split);
});

// --- 最初の表示 ---

const draft = readStorage(DRAFT_KEY, null);
if (draft && typeof draft.text === 'string') {
    editor.value = draft.text;
    nameInput.value = draft.name || '';
    currentName = draft.currentName || '';
}

refreshDocList();
updatePreview();

// MathJax は後から読み込まれるので、準備ができたらもう一度表示する
document.addEventListener('DOMContentLoaded', () => {
    if (window.MathJax && window.MathJax.startup) {
        MathJax.startup.promise.then(updatePreview);
    }
});
