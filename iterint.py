from . import utils

@utils.edit(int, 'tp_iter')
@utils.nullwrap
def int_iter(self):
    yield from range(self)
