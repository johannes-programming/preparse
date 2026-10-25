__all__: list[str] = ["PreparseLongonlyWarning"]

from preparse.warnings.PreparseWarning import PreparseWarning


class PreparseLongonlyWarning(PreparseWarning):
    pass  # only possible for long options
