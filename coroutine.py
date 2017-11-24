
def coroutine():
    r = yield 'ping'
    print('coroutine got', r)

    r = yield 'ping2'
    print('coroutine got', r)


def main():
    c = coroutine()
    r = next(c)
    print('main got', r)

    r = c.send('pong')
    print('main got', r)

    try:
        c.send('pong2')
    except StopIteration:
        # coroutine が最後まで進んで終了するときは、
        # iterator 同様 StopIteration 例外が起きる
        print('coroutine stopped')

if __name__ == '__main__':
    main()
