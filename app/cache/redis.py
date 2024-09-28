import redis

# Initialize Redis connection - TODO: Move to a config file
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def set_refresh_token(user_email, access_token, expires_in_seconds):
    redis_client.set(access_token, user_email, ex=expires_in_seconds)


def get_user_email_by_token(access_token):
    return redis_client.get(access_token)


def delete_refresh_token(access_token):
    redis_client.delete(access_token)
