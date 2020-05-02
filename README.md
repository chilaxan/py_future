I wrote this python module to experiment with how CPython handles internal types.
It allows for the live replacement of internal methods with python ones.
Several examples are included, including ``jsdict`` and ``iterint``.

### JavaScript dictionaries
Makes python dictionary values settable via attributes

<details>
  <summary>Example Usage</summary>
  
```py
from py_future import jsdict

x = {}

x.a = 'whatever'

print(x) # {'a':'whatever'}
print(x.a) # whatever

del x.a

print(x) # {}
```

</details>

<details>
  <summary>Implementation</summary>
  
```py
# py_future/jsdict.py

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
```

</details>

### Iterable Integers (PEP 276)

Makes integers iterable
<details>
  <summary>Example Usage</summary>
  
```py
from py_future import iterint

for i in 10:
  print(i)

# prints 0 to 9
```

</details>

<details>
  <summary>Implementation</summary>
  
```py
# py_future/iterint.py

from . import _utils as utils

@utils.edit(int, 'tp_iter')
@utils.nullwrap
def int_iter(self):
    yield from range(self)
```

</details>
