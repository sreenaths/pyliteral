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

import ast
from typing import Dict

from pyliteral.core.exceptions import MaxSizeExceededError
from pyliteral.core.types import Object
from pyliteral.core.consts import MAX_SIZE


def loads(s: str, max_size: int = MAX_SIZE, vars: Dict[str, Object] = {}) -> Object:
    """ Parse a Python object from a literal string. """

    if not s:
        raise ValueError("Input string cannot be empty")

    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    if len(s) > max_size:
        raise MaxSizeExceededError(max_size)

    return ast.literal_eval(s)
