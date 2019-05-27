class OverwriteNotAllowed(IOError):
    pass


class NotFound(ValueError):
    pass


class OperationNotAllowed(PermissionError):
    pass
