# How to use pre-commit

1. Begin by installing the necessary packages from `requirements-dev.txt`:
```
pip install -r requirements-dev.txt
```
2. Next, install the git hook scripts:
```
pre-commit install
```
From now on, every time you commit, pre-commit will also run. Keep in mind that if pre-commit fixes or changes something, you'll need to stage the affected files again.

Note: Additionally, you can manually run pre-commit by executing `pre-commit run`.
