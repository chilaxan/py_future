from . import _utils as utils

@utils.edit(tuple, 'tp_str')
@utils.nullwrap
def tuple_str(self):
    return ''.join(map(str,self))

@utils.edit(list, 'tp_str')
@utils.nullwrap
def list_str(self):
    return ''.join(map(str,self))
