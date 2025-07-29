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

class MaxSizeExceededError(Exception):
    """Raised when the input exceeds the maximum allowed size."""

    def __init__(self, max_size: int):
        super().__init__(f"Input exceeds maximum size of {max_size} characters.")
        self.max_size = max_size
