#!/usr/bin/env bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

set -euxo pipefail

source tests/scripts/setup-pytest-env.sh

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui/auth

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui/controller

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui/forms

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui/screens

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/gui/widgets

echo "Checking MyPy Type defs in the TensorIR schedule package."
mypy  --check-untyped-defs src/globals

# echo "Checking MyPy Type defs in the TensorIR schedule package."
# mypy  --check-untyped-defs src/operator
