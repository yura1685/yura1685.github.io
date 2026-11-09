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

## Previewing locally (VS Code Live Server)

The pages use Jekyll (layouts, `{% include %}`, front matter), which Live Server cannot run by itself.
So Jekyll builds the finished site into `_site/`, and Live Server shows `_site/` (set in `.vscode/settings.json`).

First time only:

1. Install Ruby (Windows: "Ruby+Devkit" from https://rubyinstaller.org/ , Mac: `brew install ruby`).
2. In this folder, run `bundle install`.

Each time:

1. Run `bundle exec jekyll build --watch` in a terminal (or VS Code: Terminal → Run Task → "Jekyll 自動ビルド") and keep it running.
2. Click "Go Live" as usual. Saving a file rebuilds `_site/` and Live Server reloads the page.

Edit the files in the main folder, not in `_site/` (it is overwritten on every build).
`bundle exec jekyll serve` (http://127.0.0.1:4000) also works without Live Server.
