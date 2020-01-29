# Makes strings auto join on lists and tuples -> str([1,2]) == '12'

from . import _utils as utils

@utils.edit(tuple, 'tp_str')
@utils.nullwrap
def tuple_str(self):
    return ''.join(map(str,self))

@utils.edit(list, 'tp_str')
@utils.nullwrap
def list_str(self):
    return ''.join(map(str,self))
