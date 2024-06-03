"""
The "with" statement and the context manager.

Source:
Alex Martelli, Anna Martelli Ravenscroft, Steve Holden, and Paul McGuire,
"Python in a Nutshell: A Desktop Quick Reference", O'Reilly Media, 2023

See also:
https://docs.python.org/3/library/contextlib.html
"""
from contextlib import contextmanager

"""
with expression [as varname] [, ...]:
    ...
"""

# 3.10+ multiple context managers for a with statement can be enclosed in parentheses
"""
with (expression [as varname], ...):
    ...
"""

# The semantics of "with" are equivalent to:
"""
_normal_exit = True
_manager = expression
varname = _manager.__enter__()

try:
    ...
    
except:
    _normal_exit = False
    if not _manager.__exit__(*sys.exc_info()):
        # Note that exception does not propagate if __exit__ returns a true value
        raise ...

finally:
    if _normal_exit:
        _manager.__exit__(None, None, None)
"""


class enclosing_tag:
    """
    Here is a simple, purely illustrative way to ensure
    <name> and </name> tags are printed around some other output.
    Note that context manager classes often have lowercase names.
    """
    def __init__(self, tagname):
        self._tagname = tagname

    def __enter__(self):
        print(f'<{self._tagname}>', end='')

    def __exit__(self, et, ev, etb):
        """
        Args:
            et: exception type
            ev: exception value
            etb: exception traceback
        """
        print(f'</{self._tagname}>')


with enclosing_tag('sometag'):
    ...
# <sometag></sometag>


# Alternatively turn a generator function into a factory of
# context manager objects using the @contextlib.contextmanager decorator
@contextmanager
def enclosing_tag_2(tagname):
    print(f'<{tagname}>', end='')
    try:
        yield
    finally:
        print(f'</{tagname}>')


with enclosing_tag_2('sometag_2'):
    ...
# <sometag_2></sometag_2>


@contextmanager
def enclosing_tag_3(tagname):
    print(f'<{tagname}>', end='')
    resource = "some_resource"
    try:
        yield resource
    finally:
        print(f'</{tagname}>')


with enclosing_tag_3('sometag_3') as res:
    print(res, end='')
# <sometag_3>some_resource</sometag_3>

with enclosing_tag_3('sometag_3_1') as res:
    print(res, end='')
# <sometag_3_1>some_resource</sometag_3_1>
