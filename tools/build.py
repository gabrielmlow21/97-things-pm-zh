"""Build the Chinese site from the English originals and translation-src/*.txt.

Usage: python3 tools/build.py tools/source-en translation-src docs
"""
import sys, re, os, glob, html, shutil
src, tdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = 'https://yoshi389111.github.io/kinokobooks/'
LIC = '<a href="https://creativecommons.org/licenses/by/3.0/us/" rel="nofollow">知识共享 署名 3.0 美国（CC BY 3.0 US）</a>'

def amp(s): return re.sub(r'&(?![a-zA-Z]+;|#x?[0-9a-fA-F]+;)', '&amp;', s)
def strip(s): return html.unescape(re.sub(r'<[^>]+>', '', s))

trans = {}
for p in sorted(glob.glob(os.path.join(tdir, '*.txt'))):
    for chunk in re.split(r'^=== ', open(p, encoding='utf-8').read(), flags=re.M)[1:]:
        name, _, rest = chunk.partition('\n')
        lines = rest.strip().split('\n')
        assert lines[0].startswith('# '), (p, name)
        blocks = re.split(r'\n\s*\n', '\n'.join(lines[1:]).strip())
        trans[name.strip()] = (lines[0][2:].strip(), blocks)

def render(blocks):
    outb = []
    for b in blocks:
        ls = [l.strip() for l in b.strip().split('\n') if l.strip()]
        if all(l.startswith('- ') for l in ls):
            outb.append('<ul>\n' + ''.join(f'<li>{amp(l[2:])}</li>\n' for l in ls) + '</ul>')
        elif all(re.match(r'\d+\. ', l) for l in ls):
            outb.append('<ol>\n' + ''.join(f'<li>{amp(l.split(" ",1)[1])}</li>\n' for l in ls) + '</ol>')
        else:
            outb.append('<p>' + amp(''.join(ls)) + '</p>')
    return '\n'.join(outb)

HEAD = '''<!DOCTYPE html>
<html lang="zh-CN" prefix="og: http://ogp.me/ns#">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="../css/style_zh.css"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
<title>{title}</title>
<meta property="og:title" content="{ogtitle}">
<meta property="og:type" content="{ogtype}">
<meta property="og:image" content="{base}images/mngr97_en.png">
{extra}<meta property="og:locale" content="zh_CN">
<script type="text/javascript" src="../js/darkmode.js"></script>
</head>
<body>
'''
BOOK = '项目经理应该知道的 97 件事'
os.makedirs(os.path.join(out, 'mngr_zh'), exist_ok=True)
order = re.findall(r'<li><a href="([^"]+)">(.*?)</a> by (.*)', open(os.path.join(src, 'index.html'), encoding='utf-8').read())
missing = []
items = []
for i, (f, en_title, author) in enumerate(order):
    if f not in trans:
        missing.append(f); items.append(f'<li><a href="../mngr_en/{f}">{en_title}</a>（未翻译） {author}'); continue
    zt, blocks = trans[f]
    e = open(os.path.join(src, 'en', f), encoding='utf-8').read()
    header = re.search(r'<h1>.*?</h1>\s*(.*?)\s*</header>', e, re.S).group(1)
    prev = order[i-1][0] if i > 0 else None
    nxt = order[i+1][0] if i + 1 < len(order) else None
    nav = ['<li><a href="index.html">目录</a></li>']
    if prev: nav.insert(0, f'<li><a href="{prev}">« 上一篇</a></li>')
    if nxt: nav.append(f'<li><a href="{nxt}">下一篇 »</a></li>')
    page = HEAD.format(title=html.escape(strip(zt)) + ' - ' + BOOK, ogtitle=html.escape(strip(zt)), ogtype='article', base=BASE,
                       extra=f'<meta property="og:site_name" content="{BOOK}">\n') + f'''<article>
<header>
<h1>{amp(zt)}</h1>

{header}
</header>

{render(blocks)}

<footer>
<p class="license">原文：<a href="{BASE}mngr_en/{f}">{en_title}</a>（{author.strip()}）。本中文译文与原文一样，采用 {LIC} 许可协议。</p>
<nav>
<ul class="nav-links">
{chr(10).join(nav)}
</ul>
</nav>
</footer>
</article>
</body>
</html>
'''
    open(os.path.join(out, 'mngr_zh', f), 'w', encoding='utf-8').write(page)
    items.append(f'<li><a href="{f}">{amp(zt)}</a> —— {author.strip()}')

idx = HEAD.format(title=BOOK, ogtitle=BOOK, ogtype='website', base=BASE, extra='') + f'''<h1>{BOOK}<span id="color-scheme"></span></h1>

<p class="subtitle">《97 Things Every Project Manager Should Know》中文译本</p>

<ol>
{chr(10).join(items)}
</ol>

<footer>
<p class="license">各篇文章采用 {LIC} 许可协议。译自 <a href="{BASE}mngr_en/">英文原版</a>，作者署名保留原文。</p>
<nav>
<ul class="nav-links">
<li class="return-index"><a href="{BASE}">书籍列表</a></li>
</ul>
</nav>
</footer>

</body>
</html>
'''
open(os.path.join(out, 'mngr_zh', 'index.html'), 'w', encoding='utf-8').write(idx)
os.makedirs(os.path.join(out, 'css'), exist_ok=True); os.makedirs(os.path.join(out, 'js'), exist_ok=True)
css = open(os.path.join(src, 'css', 'style_en.css'), encoding='utf-8').read()
css = css.replace('font-family: "Helvetica",Arial,sans-serif;', 'font-family: "PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC","Noto Sans CJK SC","Helvetica",Arial,sans-serif;', 1)
css += '\np.subtitle { color: #666; }\nul.nav-links li { margin-right: 1em; }\nbody { line-height: 1.8; }\n'
open(os.path.join(out, 'css', 'style_zh.css'), 'w', encoding='utf-8').write(css)
shutil.copy(os.path.join(src, 'js', 'darkmode.js'), os.path.join(out, 'js', 'darkmode.js'))
print(f'built {len(order)-len(missing)} essays; missing {len(missing)}')
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
    '<meta http-equiv="refresh" content="0; url=mngr_zh/">\n<title>' + BOOK + '</title>\n</head>\n'
    '<body><p><a href="mngr_zh/">' + BOOK + '</a></p></body>\n</html>\n')
open(os.path.join(out, '.nojekyll'), 'w').close()
