import sys, re, html, os
src = sys.argv[1]; files = sys.argv[2:]
for f in files:
    t = open(os.path.join(src, f), encoding='utf-8').read()
    title = re.search(r'<h1>(.*?)</h1>', t, re.S).group(1)
    body = t.split('</header>',1)[1].split('<footer>',1)[0]
    body = re.sub(r'\s*</p>\s*', '', body)
    body = re.sub(r'\s*<p>\s*', '\n\n', body)
    body = re.sub(r'<ol>(.*?)</ol>', lambda m: re.sub(r'\s*<li>\s*', '\n1. ', m.group(1)), body, flags=re.S)
    body = re.sub(r'</?ul>|</li>|<br/?>', '', body)
    body = re.sub(r'\s*<li>\s*', '\n- ', body)
    body = html.unescape(body)
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    print(f'=== {f} | {html.unescape(title)}\n{body}\n')
