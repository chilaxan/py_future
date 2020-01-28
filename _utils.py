from . import _structs as structs
import ctypes
import sys

class Null:
    '''placeholder null singleton (not actually a null value)'''
    def __bool__(self):
        return False

Null = Null()

def nullwrap(func):
    '''Wraps a function to allow it to be passed null py_objects.'''
    ret = func.__annotations__.get('return') or 'py_object'
    def wrapper(*args) -> ret:
        return func(*map(lambda arg:ctypes.cast(arg, ctypes.py_object).value if arg else Null, args))
    for i in range(func.__code__.co_argcount):
        dict.__setitem__(wrapper.__annotations__, i, 'c_void_p')
    return wrapper

def get_cfunc_wrapper(func, intret=False, nullret=False, argcount=None):
    '''
    Attempts to get the appropriate CFUNCTYPE wrapper for the passed python function using annotations
    The ctype annotation can be the str name or the type
    '''
    if hasattr(func, '__annotations__') and func.__annotations__:
        ret = func.__annotations__.pop('return')
        restype = getattr(ctypes, ret) if type(ret) == str else ret
        argtypes = [getattr(ctypes, val) if type(val) == str else val for key, val in func.__annotations__.items()]
    else:
        if intret:
            restype = ctypes.c_int
        elif nullret:
            restype = None
        else:
            restype = ctypes.py_object
        argtypes = [ctypes.py_object]*(argcount or func.__code__.co_argcount)
    return ctypes.CFUNCTYPE(
        restype,
        *argtypes
    )

def edit(cls, attr=None, name=None, cfunc_wrapper=None, intret=False, nullret=False, argcount=None):
    '''Decorator that allows for the modification of python base types'''
    cls_struct = structs.c_typeobj(cls)
    def dec(func):
        nonlocal cfunc_wrapper, cls_struct
        if attr is None:
            if name is None:
                raise Exception('Invalid Arguments, [name] must be set if [attr] is None')
            dict.__setitem__(cls_struct.tp_dict, name, func)
            return func
        spec_struct = {
            'nb': ('tp_as_number', structs.PyNumberMethods),
            'sq': ('tp_as_sequence', structs.PySequenceMethods),
            'mp': ('tp_as_mapping', structs.PyMappingMethods),
            'bf': ('tp_as_buffer', structs.PyBufferProcs)
        }.get(attr[:2])
        if spec_struct:
            spec_addr = getattr(cls_struct, spec_struct[0])
            if spec_addr is None:
                new_s = tuple.__getitem__(spec_struct, 1)()
                obj = structs.c_obj(new_s)
                obj.ob_refcnt = int.__add__(obj.ob_refcnt, 1)
                setattr(cls_struct, tuple.__getitem__(spec_struct, 0), id(new_s))
            cls_struct = tuple.__getitem__(spec_struct, 1).from_address(
                getattr(
                    cls_struct,
                    tuple.__getitem__(spec_struct, 0)
                )
            )
        if cfunc_wrapper is None:
            cfunc_wrapper = get_cfunc_wrapper(func, intret, nullret, argcount)
        cfunc = cfunc_wrapper(func)
        cfunc_addr = ctypes.cast(cfunc, ctypes.c_void_p)
        if hasattr(cls_struct, attr):
            obj = structs.c_obj(cfunc)
            obj.ob_refcnt = int.__add__(obj.ob_refcnt, 1)
            setattr(cls_struct, attr, cfunc_addr)
        else:
            raise Exception('Invalid Arguments, [attr] must be a valid struct attribute')
        return cfunc
    return dec
