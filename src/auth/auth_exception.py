class UserNotFoundException(Exception):
    def __init__(self, message):
        self.msg = message


class UserExistsException(Exception):
    def __init__(self, message):
        self.msg = message


class AccessDeniedException(Exception):
    def __init__(self, message):
        self.msg = message
