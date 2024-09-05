import threading
import random
import time
from collections import deque


buffer = deque(maxlen=10)
buffer_size = 10
mutex = threading.Lock()
not_empty = threading.Condition(mutex)
not_full = threading.Condition(mutex)

# producent
def producer():
    for _ in range(100):
        item = random.randint(1, 100)
        with not_full:
            while len(buffer) >= buffer_size:
                not_full.wait()
            buffer.append(item)
            print(f'Produced: {item}')
            not_empty.notify()

# spotřebitel
def consumer():
    total_sum = 0
    for _ in range(100):
        with not_empty:
            while len(buffer) == 0:
                not_empty.wait()
            item = buffer.popleft()
            total_sum += item
            print(f'Consumed: {item}, Current Sum: {total_sum}')
            not_full.notify()
    print(f'Final Sum: {total_sum}')

# vlákna
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()
