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
- 4月から就職で渋谷に
- [PyCon APAC/Taiwan 2015 参加レポート | gihyo.jp](http://gihyo.jp/news/report/01/pycon-apac-2015)
- [PyCon APAC/Korea 2016 参加レポート | gihyo.jp](http://gihyo.jp/news/report/01/pycon-apac2016)
- [PyCon JP 2016 「基礎から学ぶWebフレームワークの作り方」](http://c-bata.link/webframework-in-python/slide.html#1)
- 神戸Pythonの会 Webアプリ開発 「Kobinハンズオン」
]

---
## Agenda

テーマ「非同期処理」

1. 非同期処理とは？
2. 非同期処理を触ってみる
3. 難しいところ

???

今日はですね、北村さんから「並行処理と非同期処理」について話して欲しいと依頼を受けたので、
Pythonにおける非同期処理をメインにお話していきます。

並行処理というのはですね、ソフトウェア工学の分野でもかなり膨大で難しいトピックでして、
それだけで何冊も本が出るほどですね。まだまだ研究されていく分野ではあるんですが、

現状、Pythonにおいて並行処理が必要になった際にどのように対処することができるのかについて今日はお話していきます。

---
## まずはとあるサーバを動かしてみる

とあるサーバにHTTPリクエストをいくつか送って、時間を計測してみる。

```python
import time

def app(environ, start_response):
    time.sleep(1)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a slow web api']
```

```console
$ gunicorn -w 2 server:app
```

レスポンスまで1秒かかるサーバ。
このようなサーバに同時に4回リクエストを送らないといけない

???
並行処理というのはソフトウェア工学の中でも結構難しいトピックと言われていて、
言葉で考えると並行とか並列とか、日本語で見ると似たような言葉がいくつか出てきます。
これ最初は結構混乱するので、まず簡単な例を見てみましょう。

今からとあるサーバにいくつかHTTPのリクエストを送ってみます。
実際にどこかのサービスのAPIとかを叩いてみてもいいんですが、
あまり負荷をかけるのもあれなので、今回は処理に1秒もかかってしまうサーバを用意しますね。

---
## 4回リクエストを送ってみる

4回のリクエストを1回ずつ投げると、4秒かかる

```console
$ hey -n 4 -c 1 http://localhost:8000
...
Summary:
  Total:        4.0223 secs
  ...
  Requests/sec: 0.9945
```

トータルで4秒かかりました。

???
では今作ったサーバに対して、実際にリクエストを送ってみましょう。
負荷をかけるツールは何でもいいんですが、apache benchとかh2loadが定番かなと思います。
今回はapache benchライクに使えるGoで書かれたheyというツールを利用しますね。
h2loadでもapache benchでも同じように使うことができて、同じような結果が返ってくると思います。

1回ずつリクエストを投げてみます。

もう少し時間を短くするには？

---
## もう少し考えてみる

この4回のリクエストは、互いに影響を与えない。
クライアントからみると、どの順番で叩いても

互いに影響を与えない2つの同時発生するイベントをどのように処理するか？

- マルチコアプロセッサや複数のマシンを最大限に活用する
- 

並行性を持つ問題に対するアプローチはいくつか存在。

- 並列に処理をする (parallel processing)
- 非同期に処理する (asynchronous processing)

同時に何かリクエストが合った時にどのように処理すればよいか。
2つのイベントが発生

???

おそらくまずここで多くの人が混乱してしまいます。
多くの人が勘違いするのは、並行処理というのは同時に2つの処理をしないといけないわけではない。
並行性ということばがあるんですが、それは何か2つのイベント

---

2つ同時にリクエストを送ると、計4回のリクエストにかかる時間は2秒になる。

```console
$ hey -n 4 -c 2 http://localhost:8000
2 requests done.
All requests done.

Summary:
  Total:        2.0088 secs
  Slowest:      1.0045 secs
  Fastest:      1.0042 secs
  Average:      1.0043 secs
  Requests/sec: 1.9913
```


---
template: inverse

## Tutorial

---
.left-column[
## Tutorial
### Hello World
]
.right-column[
まずはサーバを用意

```python
import time
from wsgiref.simple_server import make_server

def app(environ, start_response):
    time.sleep(1)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a slow web api']

if __name__ == '__main__':
    print("Serving on port 8000...")
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()
```

`server.py` という名前で保存して、

```console
$ python3.6 server.py
Serving on port 8000...
```

http://127.0.0.1:8000/ に行ってみよう。
]

---
.left-column[
## Demo
### synchronous
]
.right-column[
```python
import requests

def fetch(url):
    resp = requests.get(url)
    return resp.text

def main(url):
    results = [fetch(url) for _ in range(2)]
    return results

if __name__ == '__main__':
    results = main('http://localhost:8000/')
    for r in results:
        print(r)
```

```console
$ time python client.py 
This is a slow web api
This is a slow web api

real    0m2.195s
user    0m0.157s
sys     0m0.026s
```
]


---
.left-column[
## Demo
### synchronous
### asynchronous
]
.right-column[
```python
import aiohttp
import asyncio

async def fetch(url, l):
    async with aiohttp.ClientSession(loop=l) as session:
        async with session.get(url) as response:
            return await response.text()

async def main(url, l):
    tasks = [asyncio.ensure_future(fetch(url, l)) for _ in range(2)]
    return await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main('http://localhost:8000', loop))
    for r in results:
        print(r)
```

```console
$ time python async_client.py 
This is a slow web api
This is a slow web api

real    0m1.366s
user    0m0.309s
sys     0m0.044s
```
]
---
template: inverse

## Q&A

