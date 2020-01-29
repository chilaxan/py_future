# Makes python dictionary values settable via attributes

from . import _utils as utils

@utils.edit(dict, 'tp_getattro')
@utils.nullwrap
def dict_getattro(self, key):
    try:
        return dict.__getattribute__(self, key)
    except AttributeError as attr_err:
        err = attr_err
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            pass
    raise err

@utils.edit(dict, 'tp_setattro')
@utils.nullwrap
def dict_setattro(self, key, val) -> 'c_int':
    if val == utils.Null:
        del self[key]
        return 0
    dict.__setitem__(self, key, val)
    return 0
