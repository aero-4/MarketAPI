from redis import Redis


async def incr_with_expire(redis: Redis, key: str, window: int) -> int:
    lua = """
    local v = redis.call('INCR', KEYS[1])
    if v == 1 then
      redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    return v
    """
    val = await redis.eval(lua, 1, key, window)
    try:
        return int(val)
    except Exception:
        return 0