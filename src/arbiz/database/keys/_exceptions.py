from .._exceptions import DatabaseException


class KeysException(DatabaseException):
    pass


class NoKeys(KeysException):
    pass
