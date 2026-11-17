# 项目经理应该知道的 97 件事（中文版）

A Simplified Chinese translation of *97 Things Every Project Manager Should Know*,
based on the English web edition at
<https://yoshi389111.github.io/kinokobooks/mngr_en/>.

**Read it online:** <https://gabrielmlow21.github.io/97-things-pm-zh/>

## Layout

| Path | What it is |
| --- | --- |
| `docs/` | The built website (served by GitHub Pages) |
| `translation-src/` | The Chinese translations, one `=== file.htm` section per essay |
| `tools/build.py` | Builds `docs/` from the English pages and the translations |
| `tools/extract.py` | Prints English essays as plain text, for translating |
| `tools/source-en/` | Copy of the English pages, stylesheet and dark-mode script |

## Rebuilding

After editing anything in `translation-src/`:

```bash
rm -rf docs && python3 tools/build.py tools/source-en translation-src docs
```

In a translation file, the first line of each section is `# 标题`; paragraphs are
separated by blank lines; lines starting with `- ` become a bulleted list and
lines starting with `1. ` a numbered list. Inline `<b>`, `<i>` and `<em>` are allowed.

## License and attribution

The essays are by their individual authors (named on each page) and are licensed
under [Creative Commons Attribution 3.0 US](https://creativecommons.org/licenses/by/3.0/us/).
This translation is a derivative work released under the same license. Each page
links to its English original. The stylesheet and dark-mode script come from
[yoshi389111/kinokobooks](https://github.com/yoshi389111/kinokobooks).
