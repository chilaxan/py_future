# Most of this file came from [https://github.com/fdintino/python-doublescript/blob/master/doublescript/structs.py]
# I have changed all the CFuncType attributes to c_void_p as to facilitate easier casting.

from ctypes import (
    POINTER, CFUNCTYPE, c_int, c_uint, c_ulong, c_char_p, c_void_p, py_object, c_ssize_t, Structure
)
import sys

def c_ptr(cls):
    ptr = POINTER(cls)

    def __getattr__(self, attr):
        if attr in dict(ptr._type_._fields_):
            if self:
                return getattr(self.contents, attr)
            else:
                return None
        else:
            return getattr(self.contents, attr)

    def __dir__(self):
        return sorted(set(
            [*self.__dict__.keys()] +
            dir(self.__class__) +
            [*dict(ptr._type_._fields_).keys()]))

    ptr.__getattr__ = __getattr__
    ptr.__dir__ = __dir__
    return ptr


c_int_p = c_ptr(c_int)
c_char_p_p = c_ptr(c_char_p)
c_void_p_p = c_ptr(c_void_p)
c_file_p = c_void_p
py_object_p = c_ptr(py_object)


Py_ssize_t_p = c_ptr(c_ssize_t)
Py_hash_t = c_ssize_t


class NullSafeStructure(Structure):

    def __getattribute__(self, attr):
        try:
            return super(NullSafeStructure, self).__getattribute__(attr)
        except ValueError as e:
            if ("%s" % e).endswith('is NULL'):
                return None
            else:
                raise e

class PyObject(NullSafeStructure):
    pass


PyObject_fields = [
    ('ob_refcnt', c_ssize_t),
    ('ob_type', py_object),
]

if hasattr(sys, 'getobjects'):
    PyObject_fields = [
        ('_ob_next', c_ptr(PyObject)),
        ('_ob_prev', c_ptr(PyObject)),
    ] + PyObject_fields


PyObject._fields_ = PyObject_fields


class PyVarObject(PyObject):
    """ PyObject_VAR_HEAD """
    _fields_ = [('ob_size', c_ssize_t)]


PyVarObject_p = c_ptr(PyVarObject)

unaryfunc = CFUNCTYPE(py_object, py_object)
binaryfunc = CFUNCTYPE(py_object, py_object, py_object)
ternaryfunc = CFUNCTYPE(py_object, py_object, py_object, py_object)
inquiry = CFUNCTYPE(c_int, py_object)
lenfunc = CFUNCTYPE(c_ssize_t, py_object)
coercion = CFUNCTYPE(c_int, py_object_p, py_object_p)
ssizeargfunc = CFUNCTYPE(py_object, py_object, c_ssize_t)
ssizessizeargfunc = CFUNCTYPE(py_object, py_object, c_ssize_t, c_ssize_t)
intobjargproc = CFUNCTYPE(c_int, py_object, c_int, py_object)
intintobjargproc = CFUNCTYPE(c_int, py_object, c_int, c_int, py_object)
ssizeobjargproc = CFUNCTYPE(c_int, py_object, c_ssize_t, py_object)
ssizessizeobjargproc = CFUNCTYPE(c_int, py_object, c_ssize_t, c_ssize_t, py_object)
objobjargproc = CFUNCTYPE(c_int, py_object, py_object, py_object)
getreadbufferproc = CFUNCTYPE(c_int, py_object, c_int, c_void_p_p)
getwritebufferproc = CFUNCTYPE(c_int, py_object, c_int, c_void_p_p)
getsegcountproc = CFUNCTYPE(c_int, py_object, c_int_p)
getcharbufferproc = CFUNCTYPE(c_int, py_object, c_int, c_char_p_p)
readbufferproc = CFUNCTYPE(c_ssize_t, py_object, c_ssize_t, c_void_p_p)
writebufferproc = CFUNCTYPE(c_ssize_t, py_object, c_ssize_t, c_void_p_p)
segcountproc = CFUNCTYPE(c_ssize_t, py_object, Py_ssize_t_p)
charbufferproc = CFUNCTYPE(c_ssize_t, py_object, c_ssize_t, c_char_p_p)


class bufferinfo(NullSafeStructure):
    _fields_ = [
        ('buf', c_void_p),
        ('obj', py_object),
        ('len', c_ssize_t),
        ('itemsize', c_ssize_t),
        ('readonly', c_int),
        ('ndim', c_int),
        ('format', c_char_p),
        ('shape', Py_ssize_t_p),
        ('strides', Py_ssize_t_p),
        ('suboffsets', Py_ssize_t_p),
        ('smalltable', c_ssize_t * 2),
        ('internal', c_void_p),
    ]


bufferinfo_p = c_ptr(bufferinfo)
Py_buffer = bufferinfo
Py_buffer_p = c_ptr(Py_buffer)
getbufferproc = CFUNCTYPE(c_int, py_object, Py_buffer_p, c_int)
releasebufferproc = CFUNCTYPE(None, py_object, Py_buffer_p)
objobjproc = CFUNCTYPE(c_int, py_object, py_object)
visitproc = CFUNCTYPE(c_int, py_object, c_void_p)
traverseproc = CFUNCTYPE(c_int, py_object, visitproc, c_void_p)


class PyNumberMethods(NullSafeStructure):
    _fields_ = [
        ('nb_add', c_void_p),
        ('nb_subtract', c_void_p),
        ('nb_multiply', c_void_p),
        ('nb_remainder', c_void_p),
        ('nb_divmod', c_void_p),
        ('nb_power', c_void_p),
        ('nb_negative', c_void_p),
        ('nb_positive', c_void_p),
        ('nb_absolute', c_void_p),
        ('nb_bool', c_void_p),  # nb_nonzero in python 2
        ('nb_invert', c_void_p),
        ('nb_lshift', c_void_p),
        ('nb_rshift', c_void_p),
        ('nb_and', c_void_p),
        ('nb_xor', c_void_p),
        ('nb_or', c_void_p),
        ('nb_int', c_void_p),
        ('nb_long', c_void_p),  # nb_reserved in python 3
        ('nb_float', c_void_p),
        ('nb_inplace_add', c_void_p),
        ('nb_inplace_subtract', c_void_p),
        ('nb_inplace_multiply', c_void_p),
        ('nb_inplace_remainder', c_void_p),
        ('nb_inplace_power', c_void_p),
        ('nb_inplace_lshift', c_void_p),
        ('nb_inplace_rshift', c_void_p),
        ('nb_inplace_and', c_void_p),
        ('nb_inplace_xor', c_void_p),
        ('nb_inplace_or', c_void_p),
        ('nb_floor_divide', c_void_p),
        ('nb_true_divide', c_void_p),
        ('nb_inplace_floor_divide', c_void_p),
        ('nb_inplace_true_divide', c_void_p),
        ('nb_index', c_void_p),
        ('nb_matrix_multiply', c_void_p),
        ('nb_inplace_matrix_multiple', c_void_p),
    ]


PyNumberMethods_p = c_ptr(PyNumberMethods)


class PySequenceMethods(NullSafeStructure):
    """
    lenfunc sq_length;
     binaryfunc sq_concat;
     ssizeargfunc sq_repeat;
     ssizeargfunc sq_item;
     ssizessizeargfunc sq_slice;
     ssizeobjargproc sq_ass_item;
     ssizessizeobjargproc sq_ass_slice;
     objobjproc sq_contains;
     binaryfunc sq_inplace_concat;
     ssizeargfunc sq_inplace_repeat;
    """
    _fields_ = [
        ('sq_length', c_void_p),
        ('sq_concat', c_void_p),
        ('sq_repeat', c_void_p),
        ('sq_item', c_void_p),
        ('sq_slice', c_void_p),  # was_sq_slice in python 3
        ('sq_ass_item', c_void_p),
        ('sq_ass_slice', c_void_p),  # was_sq_ass_slice in python 3
        ('sq_contains', c_void_p),
        ('sq_inplace_concat', c_void_p),
        ('sq_inplace_repeat', c_void_p),
    ]


PySequenceMethods_p = c_ptr(PySequenceMethods)


class PyMappingMethods(NullSafeStructure):
    _fields_ = [
        ('mp_length', c_void_p),
        ('mp_subscript', c_void_p),
        ('mp_ass_subscript', c_void_p),
    ]


PyMappingMethods_p = c_ptr(PyMappingMethods)


class PyAsyncMethods(NullSafeStructure):
    _fields_ = [
        ('am_await', c_void_p),
        ('am_aiter', c_void_p),
        ('am_anext', c_void_p),
    ]


PyAsyncMethods_p = c_ptr(PyAsyncMethods)


class PyBufferProcs(NullSafeStructure):
    _fields_ = [
        ('bf_getreadbuffer', c_void_p),
        ('bf_getwritebuffer', c_void_p),
        ('bf_getsegcount', c_void_p),
        ('bf_getcharbuffer', c_void_p),
        ('bf_getbuffer', c_void_p),
        ('bf_releasebuffer', c_void_p),
    ]


PyBufferProcs_p = c_ptr(PyBufferProcs)
freefunc = CFUNCTYPE(None, c_void_p)
destructor = CFUNCTYPE(None, py_object)
printfunc = CFUNCTYPE(c_int, py_object, c_file_p, c_int)
getattrfunc = CFUNCTYPE(py_object, py_object, c_char_p)
getattrofunc = CFUNCTYPE(py_object, py_object, py_object)
setattrfunc = CFUNCTYPE(c_int, py_object, c_char_p, py_object)
setattrofunc = CFUNCTYPE(c_int, py_object, py_object, py_object)
cmpfunc = CFUNCTYPE(c_int, py_object, py_object)
reprfunc = CFUNCTYPE(py_object, py_object)
hashfunc = CFUNCTYPE(Py_hash_t, py_object)
richcmpfunc = CFUNCTYPE(py_object, py_object, py_object, c_int)
getiterfunc = CFUNCTYPE(py_object, py_object)
iternextfunc = CFUNCTYPE(py_object, py_object)
descrgetfunc = CFUNCTYPE(py_object, py_object, py_object, py_object)
descrsetfunc = CFUNCTYPE(c_int, py_object, py_object, py_object)
initproc = CFUNCTYPE(c_int, py_object, py_object, py_object)


class PyTypeObject(NullSafeStructure):
    pass


PyTypeObject_p = c_ptr(PyTypeObject)

newfunc = CFUNCTYPE(py_object, PyTypeObject_p, py_object, py_object)
allocfunc = CFUNCTYPE(py_object, PyTypeObject_p, c_ssize_t)

PyTypeObject._fields_ = [
    ('ob_refcnt', c_ssize_t),
    ('ob_type', py_object),
] + PyObject_fields[2:] + [
    ('ob_size', c_ssize_t),
    ('tp_name', c_char_p),
    ('tp_basicsize', c_ssize_t),
    ('tp_itemsize', c_ssize_t),
    ('tp_dealloc', destructor),
    ('tp_print', c_void_p),
    ('tp_getattr', c_void_p),
    ('tp_setattr', c_void_p),
    # tp_compare is tp_as_async in python 3.5, tp_reserved in earlier python 3
    ('tp_compare', c_void_p),
    ('tp_repr', c_void_p),
    ('tp_as_number', c_void_p),
    ('tp_as_sequence', c_void_p),
    ('tp_as_mapping', c_void_p),
    ('tp_hash', c_void_p),
    ('tp_call', c_void_p),
    ('tp_str', c_void_p),
    ('tp_getattro', c_void_p),
    ('tp_setattro', c_void_p),
    ('tp_as_buffer', c_void_p),
    ('tp_flags', c_ulong),
    ('tp_doc', c_char_p),
    ('tp_traverse', c_void_p),
    ('tp_clear', c_void_p),
    ('tp_richcompare', c_void_p),
    ('tp_weaklistoffset', c_ssize_t),
    ('tp_iter', c_void_p),
    ('tp_iternext', c_void_p),
    ('tp_methods', c_void_p),
    ('tp_members', c_void_p),
    ('tp_getset', c_void_p),
    ('tp_base', py_object),
    ('tp_dict', py_object),
    ('tp_descr_get', c_void_p),
    ('tp_descr_set', c_void_p),
    ('tp_dictoffset', c_ssize_t),
    ('tp_init', c_void_p),
    ('tp_alloc', c_void_p),
    ('tp_new', c_void_p),
    ('tp_free', c_void_p),
    ('tp_is_gc', c_void_p),
    ('tp_bases', py_object),
    ('tp_mro', py_object),
    ('tp_cache', py_object),
    ('tp_subclasses', py_object),
    ('tp_weaklist', py_object),
    ('tp_del', c_void_p),
    ('tp_version_tag', c_uint),
]


class PyClassObject(NullSafeStructure):
    _fields_ = [
        ('ob_refcnt', c_ssize_t),
        ('ob_type', py_object),
        ('cl_bases', py_object),
        ('cl_dict', py_object),
        ('cl_name', py_object),
        ('cl_getattr', py_object),
        ('cl_setattr', py_object),
        ('cl_delattr', py_object),
        ('cl_weakreflist', py_object),
    ]


class PyInstanceObject(NullSafeStructure):
    _fields_ = [
        ('ob_refcnt', c_ssize_t),
        ('ob_type', py_object),
        ('in_class', py_object),
        ('in_dict', py_object),
        ('in_weakreflist', py_object),
    ]


class PyFunctionObject(NullSafeStructure):
    _fields_ = [
        ('ob_refcnt', c_ssize_t),
        ('ob_type', py_object),
        ('func_code', py_object),
        ('func_defaults', py_object),
        ('func_closure', py_object),
        ('func_doc', py_object),
        ('func_name', py_object),
        ('func_dict', py_object),
        ('func_weakreflist', py_object),
        ('func_module', py_object),
    ]


wrapperfunc = CFUNCTYPE(py_object, py_object, py_object, c_void_p)


class PyDescrObject(NullSafeStructure):
    _fields_ = PyObject_fields + [
        ('d_type', py_object),
        ('d_name', py_object),
        ('d_qualname', py_object)
    ]


class wrapperbase(NullSafeStructure):
    _fields_ = [
        ('name', c_char_p),
        ('offset', c_int),
        ('function', c_void_p),
        ('wrapper', c_void_p),
        ('doc', c_char_p),
        ('flags', c_int),
        ('name_strobj', py_object),
    ]


class PyWrapperDescrObject(NullSafeStructure):
    _fields_ = PyDescrObject._fields_ + [
        ('d_base', c_ptr(wrapperbase)),
        ('d_wrapped', c_void_p),
    ]


class CDataObject(NullSafeStructure):
    pass


CDataObject._fields_ = PyObject_fields + [
    ('b_ptr', POINTER(c_void_p)),
    ('b_needsfree', c_int),
    ('b_base', c_ptr(CDataObject)),
    ('b_size', c_ssize_t),
    ('b_length', c_ssize_t),
    ('b_index', c_ssize_t),
    ('b_objects', py_object),
]


class DictProxy(PyObject):
    _fields_ = [('dict', POINTER(PyObject))]


def c_typeobj(t):
    return PyTypeObject.from_address(id(t))

def c_obj(o):
    return PyObject.from_address(id(o))
