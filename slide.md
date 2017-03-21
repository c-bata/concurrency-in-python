name: inverse
layout: true
class: center, middle, inverse
---
# 並行プログラミング in Python

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
## アジェンダ

1. 同期的なアプローチ
2. マルチスレッド
3. async/awaitによる非同期処理
4. マルチプロセス
5. 手を動かしてみよう

---
.left-column[
## Demo
### Server
]
.right-column[

### サーバの準備

とあるサーバにHTTPリクエストをいくつか送って、時間を計測してみる。

```python
import time

def app(environ, start_response):
    time.sleep(1)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a slow web api']
```

見ての通り、1秒待ってからレスポンスを返すサーバです。
ワーカー数を3つで動かしてみましょう。

```console
$ gunicorn -w 3 server:app
```
]

???
今からとあるサーバにいくつかHTTPのリクエストを送ってみます。
実際にどこかのサービスのAPIとかを叩いてみてもいいんですが、
あまり負荷をかけるのも迷惑なのでサーバを用意しますね。

---
.left-column[
## Demo
### Server
### Client(sync)
]
.right-column[

### クライアントの実装(同期版)

それでは3回、HTTPリクエストを送ってみます。

```python
import requests

def main():
    urls = ['http://localhost:8000' for _ in range(3)]
    for u in urls:
        r = requests.get(u)
        print(r.text)

if __name__ == '__main__':
    main()
```

結果: **3秒** ちょっと

```console
$ time python client_sync.py 
This is a slow web api
This is a slow web api
This is a slow web api

real    0m3.240s
user    0m0.164s
sys     0m0.037s
```
]
???
3秒ちょっとかかりました。
今回用意したサーバは、レスポンスを返すのに1秒かかるので、ごく自然な結果ですね。
それでは時間を短縮する方法を考えてみましょう。

---
.left-column[
## Demo
### Server
### Client(sync)
### Problem
]
.right-column[
### 高速化する方法
この3回のリクエストは、互いに影響を与えない。
クライアントからみると、どの順番で叩いてもいいし、

互いに影響を与えない2つの同時発生するイベントをどのように処理するか？

- マルチコアプロセッサや複数のマシンを最大限に活用する
- 

並行性を持つ問題に対するアプローチはいくつか存在。

- 並列に処理をする (parallel processing)
- 非同期に処理する (asynchronous processing)

同時に何かリクエストが合った時にどのように処理すればよいか。
2つのイベントが発生
]

???
おそらくまずここで多くの人が混乱してしまいます。
多くの人が勘違いするのは、並行処理というのは同時に2つの処理をしないといけないわけではない。
並行性ということばがあるんですが、それは何か2つのイベント

---
### マルチスレッド

複数のスレッドを使うことで、次のように効率化できそうです。

![multi-thread](./img/multi-thread.png)

それではマルチスレッドを用いて、高速化してみましょう。
いくつかの危険性をもつ実装ですが、素直に書くとこのように書いてしまうかもしれません。

---
template: inverse

## Q&A

