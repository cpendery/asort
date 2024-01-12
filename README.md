# asort

> [!IMPORTANT]  
> `asort` has been deprecated and is getting integrated into [ruff](https://github.com/astral-sh/ruff). Track the progress [here](https://github.com/astral-sh/ruff/issues/1198).

[![PyPI version](https://badge.fury.io/py/asort.svg)](https://badge.fury.io/py/asort)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cpendery/asort/blob/main/LICENSE)
[![ASort CI](https://github.com/cpendery/asort/workflows/ASort%20CI/badge.svg)](https://github.com/cpendery/asort/actions/workflows/asort-ci.yaml)
[![codecov](https://codecov.io/gh/cpendery/asort/branch/main/graph/badge.svg)](https://codecov.io/gh/cpendery/asort)
[![Downloads](https://img.shields.io/pypi/dm/asort)](https://pypistats.org/packages/asort)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)]("https://github.com/psf/black")
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6119/badge)](https://bestpractices.coreinfrastructure.org/projects/6119)
[![DeepSource](https://deepsource.io/gh/cpendery/asort.svg/?label=active+issues&token=wY22LJbdg6Q-1V2Dd6d8Nljg)](https://deepsource.io/gh/cpendery/asort/?ref=repository-badge)

asort for `__all__` your `__all__` lists

asort is a Python utility / library to sort imports items in an `__all__` list alphabetically
It provides a command line utility, Python library and pre-commit support to
quickly sort all your imports. It requires Python 3.7+ to run but supports formatting
any version of Python code.

Works seemlessly with [black](https://github.com/psf/black) and [isort](https://github.com/PyCQA/isort) with no configuration needed

Before asort:

```python
from my_lib import Object
from my_lib import Object3
from my_lib import Object2

__all__ = [
  "Object",
  "Object3",
  "Object2",
]

```

After asort:

```python
from my_lib import Object
from my_lib import Object3
from my_lib import Object2

__all__ = [
  "Object",
  "Object2",
  "Object3",
]
```

## Installing asort

Installing asort is as simple as:

```bash
pip install asort
```

## Using asort
See usage examples on our [documentation](https://asort.readthedocs.io/en/latest/)
