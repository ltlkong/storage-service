def success(message: str, data, code = 200, custom=False):
    if code > 300 or code < 200:
        raise ValueError('Logic error')

    if custom:
        return data, code

    return {
        'message':message,
        'data':data
    }, code
