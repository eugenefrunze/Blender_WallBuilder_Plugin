import time
from tracemalloc import start
b = [i for i in range(10000000)]
c = {x: str(x) for x in range(10000000)}

start_t = time.time()
print(c[9999998])
print(time.time() - start_t)

start_t = time.time()
print(b[9999998])
print(time.time() - start_t)