from redis import Redis


def get_redis(host: str, port: int, db: int = 1) -> Redis:
    redis = Redis(host=host, port=port, db=db, decode_responses=True)
    yield redis
    redis.close()
