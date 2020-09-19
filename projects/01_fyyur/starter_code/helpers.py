import functools


def aggregate_venues(venues):
    d = functools.reduce(from_list_to_dict, venues, {})
    return [
        {
            'city': k.split('|')[0],
            'state': k.split('|')[1],
            'venues': d[k]
        } for k in d
    ]


def from_list_to_dict(a, c):
    try:
        a[f'{c["city"]}|{c["state"]}'].append(c)
    except:
        a[f'{c["city"]}|{c["state"]}'] = []
        a[f'{c["city"]}|{c["state"]}'].append(c)
    return a
