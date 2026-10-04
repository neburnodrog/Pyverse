class PyverseError(ValueError):
    """Raised for input Pyverse cannot read as a verse.

    Subclasses ValueError so that callers written against the errors this
    package used to leak keep working.
    """
