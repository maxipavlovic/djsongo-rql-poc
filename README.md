Djsongo RQL PoC
==========

This is a PoC with a nice idea to apply RQL filtering for JSON objects
with a crazy, yet working implementation through SQL.

Requirements
==========

Python 3.9+ (or below with support of JSON1 extension for SQLite)


Trying out
==========

```commandline
pip install -r requirements.txt
python manage.py migrate
python manage.py shell
```
```python
>>> from djson_rql.main import test_filter_by_query
>>> test_filter_by_query('product.id=PRD-100')
>>> test_filter_by_query('product.id=PRD-100-200')
{'id': 'ID-123', 'product': {'id': 'PRD-100-200'}, ...}
```

It works! When the function finds a match by query, the object is returned.
