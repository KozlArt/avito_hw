import io
import json
import urllib.request
from unittest.mock import patch

import pytest

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год
    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    print(resp_json)
    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


@pytest.mark.parametrize('response,year', [
    (r'{"$id": "1", "currentDateTime": "2022-11-19T15:08Z"}', 2022),
    (r'{"$id": "1", "currentDateTime": "2100-10-20T15:08Z"}', 2100),
    (r'{"$id": "1", "currentDateTime": "01.03.2019T15:08Z"}', 2019),
    (r'{"$id": "1", "currentDateTime": "22.05.1345T15:08Z"}', 1345),
])
def test_ymd_dmy(response, year):
    response = io.StringIO(response)
    with patch('urllib.request.urlopen', return_value=response):
        assert what_is_year_now() == year


def test_raise_exception():
    response = io.StringIO(r'{"$id": "1", "currentDateTime": "2005.12.11T15:08Z"}')
    with pytest.raises(ValueError):
        with patch('urllib.request.urlopen', return_value=response):
            what_is_year_now()
