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
# tests/test_literal_transformer.py
Tests for the `LiteralTransformer` class in the pyliteral module.
"""

import ast
import pytest

from pyliteral.literal_transformer import LiteralTransformer

# --- Helper function to evaluate AST expressions ---
def literal_eval(s: str, transformer: LiteralTransformer):
    """Evaluate a string literal using the LiteralTransformer."""
    tree: ast.Expression = ast.parse(s, mode="eval")
    tree = transformer.visit(tree)
    ast.fix_missing_locations(tree)
    return ast.literal_eval(tree.body)

# --- Test cases for LiteralTransformer ---

def test_visit_name():
    """Test visiting a Name node and replacing it with a Constant."""
    transformer = LiteralTransformer({"x": 42})
    result = literal_eval("{'x': x}", transformer)
    assert isinstance(result, dict)
    assert result["x"] == 42


def test_visit_joined_str():
    """Test visiting a JoinedStr node and evaluating it."""
    transformer = LiteralTransformer({"name": "World"})
    result = literal_eval('f"Hello, {name}!"', transformer)
    assert isinstance(result, str)
    assert result == "Hello, World!"

# --- Test error cases ---
def test_visit_unsupported_node_type():
    """Test visiting an unsupported node type raises TypeError."""
    transformer = LiteralTransformer({"x": 42})
    with pytest.raises(TypeError):
        literal_eval("set([1, 2, 3])", transformer)


def test_visit_name_not_defined():
    """Test visiting a Name node that is not defined raises NameError."""
    transformer = LiteralTransformer({})
    with pytest.raises(TypeError):
        literal_eval("x + 1", transformer)


def test_visit_joined_str_with_invalid_value():
    """Test visiting a JoinedStr with an invalid value raises ValueError."""
    transformer = LiteralTransformer({"name": "World"})
    with pytest.raises(TypeError):
        literal_eval('f"Hello, {name.upper()}"', transformer)


def test_visit_joined_str_with_multiple_values():
    """Test visiting a JoinedStr with multiple values."""
    transformer = LiteralTransformer({"name": "World", "greeting": "Hello"})
    result = literal_eval('f"{greeting}, {name}!"', transformer)
    assert isinstance(result, str)
    assert result == "Hello, World!"


def test_visit_joined_str_with_empty_values():
    """Test visiting a JoinedStr with empty values."""
    transformer = LiteralTransformer({"name": ""})
    result = literal_eval('f"Hello, {name}!"', transformer)
    assert isinstance(result, str)
    assert result == "Hello, !"


def test_visit_joined_str_with_mixed_types():
    """Test visiting a JoinedStr with mixed types."""
    transformer = LiteralTransformer({"name": "World", "count": 3})
    result = literal_eval('f"{count} times Hello, {name}!"', transformer)
    assert isinstance(result, str)
    assert result == "3 times Hello, World!"
