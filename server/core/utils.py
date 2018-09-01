TEST_DOMAINS = ('example.com', 'example.org', 'example.net', 'test.com')

TEST_PREFIX = '+1555'


def is_test_email(email):
    for domain in TEST_DOMAINS:
        if email.endswith(domain):
            return True

    return False


def get_test_email():
    return 'fake@example.com'


def is_test_phone(phone):
    if phone.startswith(TEST_PREFIX):
        return True


def get_test_phone():
    return '+15555555555'
