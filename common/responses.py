def error(message: str, code = 500):
    if code < 400 or code > 500:
        raise ValueError('Logic error')
    return {
        'message':message
    }, code

def success(message: str, data, code = 200):
    if code > 300 or code < 200:
        raise ValueError('Logic error')

    return {
        'message':message,
        'data':data
    }, code
