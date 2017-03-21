import requests


def fetch(url):
    resp = requests.get(url)
    return resp.text


def main(url, num):
    return [fetch(url) for _ in range(num)]

if __name__ == '__main__':
    results = main('http://localhost:8000/', 2)
    for r in results:
        print(r)
