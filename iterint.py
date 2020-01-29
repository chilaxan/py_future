# Makes ints iterable (PEP 276)

from . import _utils as utils

@utils.edit(int, 'tp_iter')
@utils.nullwrap
def int_iter(self):
    yield from range(self)
