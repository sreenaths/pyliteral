# Copyright 2025 Sreenath Somarajapuram

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
# tests/test_loads.py
This module tests loading Python literal expressions from various sources.
"""

import pytest
from pyliteral.core.exceptions import MaxSizeExceededError
from pyliteral.loads import loads


SAMPLE_DICT = '{"a": 1, "b": [2, 3], "c": None}'

# --- Test cases for loading various basic Python literal expressions ---

def test_loads_dict():
    result = loads(SAMPLE_DICT)
    assert isinstance(result, dict)
    assert result["a"] == 1
    assert result["b"] == [2, 3]
    assert result["c"] is None


def test_loads_list():
    s = '[1, 2, 3]'
    result = loads(s)
    assert isinstance(result, list)
    assert result == [1, 2, 3]


def test_loads_tuple():
    s = '(1, 2, 3)'
    result = loads(s)
    assert isinstance(result, tuple)
    assert result == (1, 2, 3)


def test_loads_str():
    s = '"hello"'
    result = loads(s)
    assert isinstance(result, str)
    assert result == "hello"


def test_loads_int():
    s = '42'
    result = loads(s)
    assert isinstance(result, int)
    assert result == 42


def test_loads_float():
    s = '3.14'
    result = loads(s)
    assert isinstance(result, float)
    assert result == 3.14


def test_loads_bool():
    s_true = 'True'
    s_false = 'False'
    assert loads(s_true) is True
    assert loads(s_false) is False


def test_loads_none():
    s = 'None'
    result = loads(s)
    assert result is None


def test_loads_max_size():
    result = loads(SAMPLE_DICT, max_size=100)  # Should succeed within max size
    assert isinstance(result, dict)
    assert result["a"] == 1


# --- Test special cases ---

def test_loads_with_comments():
    s = '{"x": 1, # This is a comment\n"y": 2}'
    result = loads(s)
    assert isinstance(result, dict)
    assert result["x"] == 1
    assert result["y"] == 2


def test_loads_multi_line_string():
    multi_line_str = """This is a
multi-line string."""

    s = f'{{"x": """{multi_line_str}""", "y": 2}}'
    result = loads(s)
    assert isinstance(result, dict)
    assert result["x"] == multi_line_str
    assert result["y"] == 2


def test_dict_with_single_quote_string():
    s = '{"key": \'value\', "another_key": \'another_value\'}'
    result = loads(s)
    assert isinstance(result, dict)
    assert result["key"] == "value"
    assert result["another_key"] == "another_value"


def test_loads_nested_structures():
    s = '{"a": [1, 2, 3], "b": {"c": 4}}'
    result = loads(s)
    assert isinstance(result, dict)
    assert result["a"] == [1, 2, 3]
    assert result["b"] == {"c": 4}


def test_loads_empty_dict():
    s = '{}'
    result = loads(s)
    assert isinstance(result, dict)
    assert result == {}


def test_single_quote_keys():
    s = "{'a': 1, 'b': 2}"
    result = loads(s)  # Convert single quotes to double
    assert isinstance(result, dict)
    assert result["a"] == 1
    assert result["b"] == 2

# --- Test error cases ---

def test_err_loads_none():
    with pytest.raises(ValueError):
        loads(None)


def test_err_loads_empty_string():
    with pytest.raises(ValueError):
        loads("")


def test_err_loads_invalid_type():
    with pytest.raises(TypeError):
        loads(123)


def test_err_loads_invalid_literal():
    with pytest.raises(SyntaxError):
        loads("invalid literal")


def test_err_loads_with_comments():
    with pytest.raises(SyntaxError):
        loads('{"x": 1, # This is a comment "y": 2}')


def test_err_loads_max_size():
    with pytest.raises(MaxSizeExceededError):
        loads(SAMPLE_DICT, max_size=10)  # Exceeds max size of 10 characters


def test_err_loads_dict_with_function_call():
    with pytest.raises(TypeError):
        loads('{"a": 1, "b": print("Hello")}')


def test_err_loads_function_call():
    with pytest.raises(TypeError):
        loads('print("Hello")')
