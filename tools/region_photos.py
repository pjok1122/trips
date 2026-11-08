#!/usr/bin/env python3
"""이야기 탭의 지역 섹션마다 대표 사진을 넣는다.

img/regions/credits.json 의 "<페이지>/<섹션 id>" 항목을 읽어, 해당 섹션 제목(dayhead) 바로 아래에
<figure class="rphoto"> 를 끼운다. 이미 들어간 섹션은 건너뛰므로 여러 번 돌려도 된다.
페이지를 생성기로 다시 만들었으면 이 스크립트를 한 번 더 돌린다.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS = """
  /* 이야기 탭 지역 사진 */
  .rphoto{position:relative;margin:18px 0 4px;border-radius:14px;overflow:hidden;aspect-ratio:16/7;background:#DCE6E3}
  .rphoto img{width:100%;height:100%;object-fit:cover;display:block}
  .rphoto figcaption{position:absolute;right:8px;bottom:7px;font-size:10.5px;line-height:1.4;color:#FBFDFC;
    background:rgba(20,32,38,.45);padding:2px 8px;border-radius:999px;max-width:80%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .rphoto figcaption a{color:inherit;text-decoration:none}
  @media (max-width:640px){.rphoto{aspect-ratio:3/2}}
"""


def short(s, n=28):
    s = re.sub(r'\s+', ' ', s).strip()
    return s if len(s) <= n else s[:n - 1] + '…'


def figure(page, rid, h, alt):
    cap = f'사진 · {html.escape(short(h["artist"]))} · {html.escape(h["lic"])}'
    return (f'\n    <figure class="rphoto" data-rphoto="{rid}">'
            f'<img src="./../img/regions/{page}/{rid}.jpg" alt="{html.escape(alt)}" loading="lazy">'
            f'<figcaption><a href="{h["page"]}">{cap}</a></figcaption></figure>')


def main():
    credits = json.load(open(os.path.join(ROOT, 'img/regions/credits.json'), encoding='utf-8'))
    pages = {}
    for key, h in credits.items():
        page, rid = key.split('/')
        pages.setdefault(page, []).append((rid, h))
    for page, items in pages.items():
        path = os.path.join(ROOT, page, 'index.html')
        s = open(path, encoding='utf-8').read()
        if '.rphoto{' not in s:
            s = s.replace('</style>', CSS + '</style>', 1)
        for rid, h in items:
            if f'data-rphoto="{rid}"' in s:
                continue
            sec = s.index(f'id="{rid}">')
            head = s.index('class="dayhead"', sec)
            end = s.index('</div>', head) + len('</div>')
            title = re.sub('<[^>]+>', '', s[head:end].split('</h2>')[0]).split('>')[-1].strip()
            s = s[:end] + figure(page, rid, h, title) + s[end:]
        open(path, 'w', encoding='utf-8').write(s)
        print(page, len(items))


if __name__ == '__main__':
    main()
