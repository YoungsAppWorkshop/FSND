import functools
from typing import List, Dict

from ..models import Category


def aggregate_categories(categories: List[Category]):
    return functools.reduce(map_categories, categories, {})


def map_categories(a: Dict, c: Category):
    a[c.id] = c.type
    return a
