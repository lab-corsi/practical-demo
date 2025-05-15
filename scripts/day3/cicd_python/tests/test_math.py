# test_app.py


import pytest
import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import custom_math 

@pytest.fixture(scope="module")
def math_sum():
    assert custom_math.sum(2,2) == 4