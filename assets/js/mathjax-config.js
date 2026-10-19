window.MathJax = {
    tex: {
        // $…$ をインライン数式にする（MathJax の初期設定では使えない）
        inlineMath: [['$', '$'], ['\\(', '\\)']]
    },
    options: {
        // 数式をクリックしたときに青い枠を出さない
        menuOptions: {
            settings: {
                enrich: false
            }
        }
    }
};
