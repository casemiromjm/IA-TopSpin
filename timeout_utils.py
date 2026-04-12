class TimeoutException(Exception):
    """Custom exception raised when the search exceeds the time limit."""
    pass

def _timeout_handler(signum, frame):
    """This function is triggered when the alarm goes off."""
    raise TimeoutException()