import requests
from threading import Thread
from queue import Queue


def fetch(url, results_queue):
    resp = requests.get(url)
    results_queue.put(resp.text)


def main():
    results_queue = Queue()

    threads = []
    urls = ['http://localhost:8000' for _ in range(3)]
    for u in urls:
        thread = Thread(target=fetch, args=[u, results_queue])
        thread.start()
        threads.append(thread)

    while threads:
        threads.pop().join()

    while not results_queue.empty():
        print(results_queue.get())

if __name__ == '__main__':
    main()
