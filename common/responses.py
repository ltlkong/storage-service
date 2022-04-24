def error(message: str,errors=None, code = 500):
    if code < 400 or code > 500:
        raise ValueError('Logic error')
    return {
        'message':message,
        'errors':errors
    }, code

def success(message: str, data, code = 200, custom=False):
    if code > 300 or code < 200:
        raise ValueError('Logic error')

    if custom:
        return data, code

    return {
        'message':message,
        'data':data
    }, code
