# Rules

## Name rules

> <h2><strong>Named rules about python pakage (kotsupy)</strong></h2>

|Item|Rule|Example|
|----|----|-------|
|Pakage|All lowercase, _ is banned, Keep short|tqdm, requests ...|
|Module|All lowercase, _ is allowed, Keep short|sys, os,...|
|Class|First uppercase, Uppercase delimited|MyFavoriteClass|
|Exception|First uppercase, Uppercase delimited|MyFuckingError|
|Variable Type|First uppercase, Uppercase delimited|MyFavoriteType|
|Method|All lowercase, using _|my_favorite_method|
|Function|All lowercase, using _|my_favorite_funcion|
|Variable|All lowercase, using _|my_favorite_instance|
|Constant|All Uppercase, using _|MY_FAVORITE_CONST|

> <h2><strong>Private writing (Accessible) </strong></h2>
|Item|Rule|Example|
|----|----|-------|
|Module|First _|_const|
|Class|First _| _MyFavoriteClass|
|Method|First _|_my_favorite_method|
|Function|First _|_my_favorite_funcion|
|Variable|First _|_my_favorite_instance|

> <h2><strong>Private writing (Unaccessible) </strong></h2>
|Item|Rule|Example|
|----|----|-------|
|Class|First __|__MyFavoriteClass|
|Method|First __|__my_favorite_method|
|Function|First __|__my_favorite_funcion|
|Variable|First __|__my_favorite_instance|

> <h2><strong>Named rules about this project</strong></h2> 

|Item|Rule|Example|
|----|----|-------|
|Directry|All lowercase, _ is allowed, Keep short|doc|
|File|All lowercase, _ is allowed, Keep short|file_config.md|
|Special file|First ., All lowercase|.lib|

## Pakage rules

> <h2><strong>Custom rules about this project</strong></h2>
|Item|Rule|
|----|----|
|Constant|Write in _const.py|
|Exception class|Write in _error.py|

> <h2><strong>How to write descriptions within python file description</strong></h2> 

Please write as follows :

(In the first of <py> file)
```python
"""
content
"""

import numpy as np
...

```

content as follows :

```python
"""
Summary
-------
Summary

See Also
----------
Some information
"""
```

> <h2><strong>How to write descriptions within python class or function description</strong></h2> 

 Please write as follows :

```python
def function()
    """
    content
    """
```

content as follows :

```python
"""
<Summary>

Parameters
----------
param : shape
    Explanation.

ex.)
x : int
    version.

Returns
-------
return : shape
    Explanation.

See Also
--------
Explanation.

Examples
--------
>>> input code
result

ex.)
>>> print(1+1)
2
"""
```
