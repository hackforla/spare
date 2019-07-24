import pytest

from core.utils import is_test_email


@pytest.mark.parametrize('email,expected', [
    ('user@example.com', True),
    ('user@gmail.com', False),
    ('user@yahoo.com', False),
    ('example@gmail.com', False),
])
@pytest.mark.django_db
def test_is_test_email(email, expected):
    assert is_test_email(email) == expected
