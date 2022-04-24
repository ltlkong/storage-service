def clear_none_in_dict(**kwargs):
    result = {k:v for k,v in kwargs.items() if v is not None}
    return result
