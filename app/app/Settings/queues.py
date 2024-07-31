from .path import env

Q_CLUSTER = {
    "name": "default",
    "workers": int(env("QUEUE_WORKER_UNITS", 1)),
    "recycle": int(env("QUEUE_RECYCLE", 100)),
    "timeout": int(env("QUEUE_TIMEOUT", 300)),
    "ack_failures": False,
    "max_attempts": int(env("QUEUE_MAX_ATTEMPTS", 3)),
    "retry": int(env("QUEUE_MAX_RETRY", 300)),
    "compress": True,
    "save_limit": 0,
    "orm": "default",
    "sync": True if env("QUEUE_SYNC") == "True" else False,
}
