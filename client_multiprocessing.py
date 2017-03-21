import requests
from multiprocessing import Pool


def fetch(url):
    resp = requests.get(url)
    return resp.text


def main():
    urls = ['http://localhost:8000' for _ in range(3)]
    with Pool(processes=3) as pool:
        results = pool.map(fetch, urls)

    for r in results:
        print(r)

if __name__ == '__main__':
    main()
