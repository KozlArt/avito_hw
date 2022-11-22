from typing import List, Tuple

import pytest


def fit_transform(*args: str) -> List[Tuple[str, List[int]]]:
    """
    fit_transform(iterable)
    fit_transform(arg1, arg2, *args)
    """
    if len(args) == 0:
        raise TypeError('expected at least 1 arguments, got 0')

    categories = args if isinstance(args[0], str) else list(args[0])
    uniq_categories = set(categories)
    bin_format = f'{{0:0{len(uniq_categories)}b}}'

    seen_categories = dict()
    transformed_rows = []

    for cat in categories:
        bin_view_cat = (int(b) for b in bin_format.format(1 << len(seen_categories)))
        seen_categories.setdefault(cat, list(bin_view_cat))
        transformed_rows.append((cat, seen_categories[cat]))

    return transformed_rows


@pytest.mark.parametrize('cities,exp_transformed_cities', [
    (['Moscow', 'New York'], [('Moscow', [0, 1]), ('New York', [1, 0])]),
    (['Moscow', 'New York', 'Moscow'], [('Moscow', [0, 1]), ('New York', [1, 0]), ('Moscow', [0, 1])])
])
def test_tf_output(cities, exp_transformed_cities):
    transformed_cities = fit_transform(*cities)
    assert exp_transformed_cities == transformed_cities


def test_raise_exception():
    cities = []
    with pytest.raises(TypeError):
        fit_transform(*cities)


def test_type():
    cities = ['Moscow', 'New York', 'Moscow']
    transformed_cities = fit_transform(*cities)
    assert isinstance(transformed_cities, list)
    assert isinstance(transformed_cities[0], tuple)
