name: inverse
layout: true
class: center, middle, inverse
---
# 非同期プログラミング in Python

Masashi Shibata (@c\_bata\_)

.footnote[Go directly to [Github](https://github.com/c-bata/asynchronous-python)]

---
layout: false
.left-column[
## Profile
.center[.profileicon[]]
]

.right-column[
こんにちは！

- 芝田 将 (Masashi Shibata)
- twitter: @c\_bata\_
- 明石高専 専攻科
- Kobin Framework開発者
- PyCon JP, Taiwan, Korea参加・登壇
    - http://gihyo.jp/news/report/01/pycon-apac-2015
    - http://gihyo.jp/news/report/01/pycon-apac2016
- PyCon JP 2016: [「基礎から学ぶWebフレームワークの作り方」](http://c-bata.link/webframework-in-python/slide.html#1)
]

---
## Agenda

1. 並行処理
2. どのような時に使うのか
3. 試してみよう

???

---
template: inverse

## 並行処理

---
template: inverse

## Tutorial

---
.left-column[
## Tutorial
### Hello World
]
.right-column[
まずは、恒例のHello World.

```python
from kobin import Kobin, Response

app = Kobin()

@app.route('/')
def hello():
    return Response('Hello World')
```

`app.py` という名前で保存して、

```console
$ wsgicli run app.py app
```

http://127.0.0.1:8000/ に行ってみよう。
]
---
template: inverse

## Q&A

