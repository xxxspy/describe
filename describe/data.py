
def des_dict(data: dict):
    parts = []
    for k,v in data.items():
        parts.append('{}={}'.format(k, v))
    return '&'.join(parts)