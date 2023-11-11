import urllib.request
import json
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
    Получает текущее время из API-worldclock и извлекает из поля
    'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


def test_ymd():
    with patch('urllib.request.urlopen') as mock_request_urlopen:
        expected_response = {'currentDateTime': '2023-01-01'}
        mock_request_urlopen.return_value \
            .__enter__.return_value.read.return_value \
            = json.dumps(expected_response)
        assert what_is_year_now() == 2023


def test_dmy():
    with patch('urllib.request.urlopen') as mock_request_urlopen:
        expected_response = {'currentDateTime': '01.01.2023'}
        mock_request_urlopen.return_value \
            .__enter__.return_value.read.return_value \
            = json.dumps(expected_response)
        assert what_is_year_now() == 2023


def test_no_date():
    with patch('urllib.request.urlopen') as mock_request_urlopen:
        expected_response = {'somethingElse': 'somethingElse'}
        mock_request_urlopen.return_value \
            .__enter__.return_value.read.return_value \
            = json.dumps(expected_response)
        with pytest.raises(KeyError):
            what_is_year_now()


def test_wrong_format_slash():
    with patch('urllib.request.urlopen') as mock_request_urlopen:
        expected_response = {'currentDateTime': '2023/01/01'}
        mock_request_urlopen.return_value \
            .__enter__.return_value.read.return_value \
            = json.dumps(expected_response)
        with pytest.raises(ValueError):
            what_is_year_now()


def test_wrong_format_no_year():
    with patch('urllib.request.urlopen') as mock_request_urlopen:
        expected_response = {'currentDateTime': '01.01'}
        mock_request_urlopen.return_value \
            .__enter__.return_value.read.return_value \
            = json.dumps(expected_response)
        with pytest.raises(IndexError):
            what_is_year_now()
