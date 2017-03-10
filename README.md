# 非同期プログラミング in Python

神戸Pythonの会発表資料。

## 環境構築

#### 用意していただくもの

- MacもしくはLinuxが動く環境
- エディタ(こだわりがない場合はPyCharmがお薦めです)
- Python 3.6


#### virtualenvの作成

ハンズオンをしていくにあたって、virtualenvの使用を推奨しています。
Python3では、 `venv` モジュールが含まれていますのでこちらを使用して作成してください。

```console
$ python3.6 -m venv venv
$ source ./venv/activate
(venv)$ which python
/<path to pwd>/venv/bin/python
(venv)$ which pip
/<path to pwd>/venv/bin/pip
```


#### 必要なライブラリのインストール

```console
(venv)$ pip install -U pip
(venv)$ pip install -c constraints.txt -r requirements.txt
```

