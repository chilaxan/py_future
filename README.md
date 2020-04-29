I wrote this python module to experiment with how CPython handles internal types. It allows for the live replacement of internal methods with python ones. Several examples are included, including ``jsdict`` and ``iterint``.
```python
from py_future import iterint

for i in 10:
  print(i)
  
# prints 0 to 9
```
