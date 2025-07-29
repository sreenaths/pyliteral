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


class LiteralTransformer(ast.NodeTransformer):
    def __init__(self, replacements):
        self.replacements = replacements
        # Define the allowed node types - Other types including Set is not allowed.
        self.allowed_node_types = (
            # Datatypes
            ast.Dict,
            ast.List,
            ast.Tuple,
            ast.Constant,

            # Structural types
            ast.Expression,
            ast.Name,
            ast.JoinedStr,
            ast.FormattedValue,
            ast.Load # Variables to be replaced
        )

    def visit(self, node):
        """Visit a node and transform it if necessary."""
        if isinstance(node, self.allowed_node_types):
            return super().visit(node)
        else:
            raise TypeError(f"Unsupported type: {type(node).__name__}")

    def visit_Name(self, node):
        """Replace variable names with their values."""
        if node.id in self.replacements:
            return ast.Constant(value=self.replacements[node.id])
        else:
            raise NameError(f"Variable name '{node.id}' is not defined")

    def visit_JoinedStr(self, node):
        # Recursively process all values inside the f-string
        values = [self.visit(v) for v in node.values]
        # Build the final string by evaluating each part
        parts = []
        for v in values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                # Evaluate the value (which should now be a Constant)
                val_node = v.value
                if isinstance(val_node, ast.Constant):
                    parts.append(str(val_node.value))
                else:
                    raise TypeError(f"Unsupported f-string value: {type(val_node).__name__}")
            else:
                # Unexpected node type
                raise ValueError(f"Unsupported f-string part: {v}")

        # Return as a Constant string node
        return ast.Constant(value="".join(parts))
