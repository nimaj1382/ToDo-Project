class MaxLimitExceededError(Exception):
    """Exception raised when a maximum limit is exceeded."""
    pass

class MaxLengthExceededError(Exception):
    """Exception raised when a field maximum length is exceeded."""
    pass

class UniquenessError(Exception):
    """Exception raised when a given field is not unique in database."""

class ExistanceError(Exception):
    """Exception raised when an object does not exist."""