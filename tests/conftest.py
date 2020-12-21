import pytest
from users_for_testing import test_users
import random


@pytest.fixture
def random_users():
    """
    A pytest fixture to get a unique random user to use in testing
    """
    users = list.copy(test_users)
    random.shuffle(users)
    return iter(users)
