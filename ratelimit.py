import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def allow(self):
        now = time.time()
        # refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

bucket = TokenBucket(capacity=5, refill_rate=1)  # 5 tokens, +1 token/sec

for i in range(10):
    if bucket.allow():
        print(f"{time.time():.2f} — allowed {i}")
    else:
        print(f"{time.time():.2f} — rate limited {i}")
    time.sleep(0.3)