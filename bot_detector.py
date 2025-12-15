import time

_last_requests = {}

def is_bot(user_id: str, user_input: str) -> bool:
    now = time.time()

    if len(user_input.strip()) < 2:
        return True

    last_time = _last_requests.get(user_id)
    _last_requests[user_id] = now

    if last_time and (now - last_time) < 0.5:
        return True

    return False
