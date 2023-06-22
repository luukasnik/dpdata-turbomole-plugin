# An example for plugin

```sh
pip install .
```

```py
import dpdata
print(dpdata.LabeledSystem(12, fmt="turbomole"))
```

The output is

```
Data Summary
Unlabeled System
-------------------
Frame Numbers     : 12
Atom Numbers      : 20
Element List      :
-------------------
X
20
```