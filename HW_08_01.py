import time
import random
from lru import LRUCache

# Функції без кешування
def range_sum_no_cache(array, left, right):
    """Повертає суму елементів без кешування."""
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    """Оновлює елемент без кешування."""
    array[index] = value


# Функції з кешем
cache = LRUCache(capacity=1000)


def range_sum_with_cache(array, left, right):
    """Повертає суму з використанням LRU-кешу."""
    key = (left, right)
    result = cache.get(key)
    if result == -1:  # cache miss
        result = sum(array[left:right + 1])
        cache.put(key, result)
    return result


def update_with_cache(array, index, value):
    """Оновлює масив і видаляє з кешу всі діапазони, що містять змінений index."""
    array[index] = value
    # інвалідація (видалення) усіх діапазонів, що охоплюють цей індекс
    keys_to_remove = [key for key in cache.cache.keys() if key[0] <= index <= key[1]]
    for key in keys_to_remove:
        del cache.cache[key]


# Генератор запитів
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        # ~3% запитів — Update
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 # ~97% — Range
            if random.random() < p_hot:       # 95% — «гарячі» діапазони
                left, right = random.choice(hot)
            else:                             # 5% — випадкові діапазони
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries


if __name__ == "__main__":
    n = 100_000
    q = 50_000

    array1 = [random.randint(1, 100) for _ in range(n)]
    array2 = array1.copy()

    queries = make_queries(n, q)

    # Тест без кешу
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_no_cache(array1, query[1], query[2])
        else:
            update_no_cache(array1, query[1], query[2])
    no_cache_time = time.time() - start

    # Тест із кешем
    start = time.time()
    for query in queries:
        if query[0] == "Range":
            range_sum_with_cache(array2, query[1], query[2])
        else:
            update_with_cache(array2, query[1], query[2])
    with_cache_time = time.time() - start

    # Результати
    speedup = no_cache_time / with_cache_time
    print(f"Без кешу : {no_cache_time:6.2f} c")
    print(f"LRU-кеш  : {with_cache_time:6.2f} c  (прискорення ×{speedup:.2f})")