# 非同期プログラミング

- Author: [Masashi Shibata (@c_bata_)](https://twitter.com/c_bata_)
- Date: 2017/03/21 (Tue)
- Event: 神戸Pythonの会

## 目次

1. 同期と非同期の違いを実際に見てみる
2. 非同期は何故速くなったのか


## 同期と非同期

まずは同期と非同期の違いについて説明する前に、とあるサーバに複数のHTTPリクエストを送る例を見てみる


### サーバーのセットアップ

今からとあるサーバにいくつかHTTPのリクエストを送ってみる。
実際にどこかのサービスのAPIとかを叩いてみてもいいんですが、
あまり負荷をかけるのも迷惑なのでサーバを用意しますね。

```python
import time

def app(environ, start_response):
    time.sleep(1)
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'This is a slow web api']
```

動かしてみましょう

```console
$ gunicorn -w 3 server:app
[2017-03-21 14:39:07 +0900] [3883] [INFO] Starting gunicorn 19.7.1
[2017-03-21 14:39:07 +0900] [3883] [INFO] Listening at: http://127.0.0.1:8000 (3883)
[2017-03-21 14:39:07 +0900] [3883] [INFO] Using worker: sync
[2017-03-21 14:39:07 +0900] [3886] [INFO] Booting worker with pid: 3886
[2017-03-21 14:39:07 +0900] [3887] [INFO] Booting worker with pid: 3887
[2017-03-21 14:39:07 +0900] [3888] [INFO] Booting worker with pid: 3888
```

### クライアント(同期版)

それではいくつかHTTPリクエストを送ってみます。
Pythonでは、requestsという有名なパッケージがあるので、こちらを使ってみましょう。

```python
import requests

def fetch(url):
    resp = requests.get(url)
    return resp.text

def main(url, num):
    return [fetch(url) for _ in range(num)]

if __name__ == '__main__':
    results = main('http://localhost:8000/', 3)
    for r in results:
        print(r)
```

実行してみます。

```console
$ time python client_sync.py 
This is a slow web api
This is a slow web api
This is a slow web api

real    0m3.219s
user    0m0.162s
sys     0m0.031s
```

**3.219s** かかりました。

今回用意したサーバは、レスポンスを返すのに1秒は必要です。
2回リクエストを送ったので2秒程度はかかるでしょう。
次は別の方法でリクエストを送ってみます。


### 非同期版クライアント

次は非同期の実装を見てみましょう。

```python
import aiohttp
import asyncio

async def fetch(l, url):
    async with aiohttp.ClientSession(loop=l) as session:
        async with session.get(url) as response:
            return await response.text()


async def main(l, url, num):
    tasks = [asyncio.ensure_future(fetch(l, url)) for _ in range(num)]
    return await asyncio.gather(*tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(loop, 'http://localhost:8000', 3))
    for r in results:
        print(r)
```

解説は後回しにしますが、実装は少し複雑なように思えますね。
とりあえず実行してみましょう。

```console
$ time python client_async.py 
This is a slow web api
This is a slow web api
This is a slow web api

real    0m1.415s
user    0m0.333s
sys     0m0.051s
```

必要な時間は、1.415sでした。
何故このようになったのでしょうか？


## 並行処理

それでは先程のプログラムのスレッドの動きを見てみましょう。

**同期版**

![同期版](./img/fetch_sync.png)

**非同期版**

![非同期版](./img/fetch_async.png)


