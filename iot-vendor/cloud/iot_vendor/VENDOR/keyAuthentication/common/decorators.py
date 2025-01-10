from functools import wraps

def api_key_auth(validator_class):
    def decorator(func):
        @wraps(func)
        def wrapper(event, *args, **kwargs):
            validator = validator_class()
            api_key = event['headers'].get('x-api-key')
            validator.validate(api_key)
            return func(event, *args, **kwargs)
        return wrapper
    return decorator