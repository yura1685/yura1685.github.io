# [yura1685's Journal](https://yura1685.github.io)

## Directory structure

- `_layouts/base.html`: shared head, menu and footer used by every page
- `_layouts/library.html`: layout for each library page (`atcoder/library/*.md`)
- `_includes/code.html`: shows a `.py` file as a code block
- `assets/css/`: site-wide CSS
- `assets/js/`: site-wide JavaScript (`csv.js` has the Google Sheets URLs, `markdown.js` renders article/solution Markdown)
- `assets/images/`: favicon and icons
- `articles/contents/`: article body files
- `articles/assets/<article-id>/`: images and PDFs used by each article
- `atcoder/solutions/`: AtCoder solution files
- `atcoder/assets/<contest>/`: images used by each solution
- `atcoder/library/`: library pages (`<name>.md`) and their code (`<name>.py`)
- `problems/`: original problems page; each problem is `_problems/<number>.txt` (front matter + Markdown statement, see `_problems/_template.txt`; `assets/js/problems.js`)
- `playground/`: live Markdown + math preview page (`assets/js/playground.js`; saves to the browser's localStorage)
