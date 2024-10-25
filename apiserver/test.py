import time
import requests

def test_search_api():
    num_tests = 100
    total_time = 0

    for i in range(num_tests):
        start = time.time()

        res = requests.get('http://127.0.0.1:33842/api/search?q=iphone')
        res.raise_for_status()

        duration = time.time() - start
        total_time += duration

    avg_time = total_time / num_tests

    print('Average search time:', avg_time)


if __name__ == '__main__':
    test_search_api()
