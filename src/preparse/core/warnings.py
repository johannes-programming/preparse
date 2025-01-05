import warnings

__all__ = [
    "PreparseWarning",
    "PreparseUnrecognizedOptionWarning",
]
class PreparseWarning(warnings.Warning):
    "This class allows all warnings from preparse "
    "to be regulated with simplefilter from warnings."
    def __init__(self, *args, prog=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prog = prog
    def __str__(self):
        leg = super().__str__()
        if self.prog is None:
            return leg
        else:
            return f"{self.prog}: {leg}"

class PreparseUnrecognizedOptionWarning(PreparseWarning):
    "Warn about an unrecognized option."
    def __init__(self, *args, prog=None, **kwargs):
        super().__init__(*args, prog=prog, **kwargs)
        self.warn("unrecognized option %r" % option)    
