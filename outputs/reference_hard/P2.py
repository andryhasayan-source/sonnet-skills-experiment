import copy

DELETE = object()

def deep_merge(base, override):
    result = {}
    for k, v in base.items():
        result[k] = copy.deepcopy(v)
    for k, v in override.items():
        if v is DELETE:
            result.pop(k, None)
            continue
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result
