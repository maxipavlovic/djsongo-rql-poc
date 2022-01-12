import re
from functools import partial
from typing import Optional

from django.db import models, transaction

from dj_rql.filter_cls import RQLFilterClass

from flatten_json import flatten

from .models import RQLJsonToSQL


@transaction.atomic(savepoint=False)
def filter_by_query(data: dict, query: Optional[str] = None) -> Optional[dict]:
    if not query:
        return data

    instance = RQLJsonToSQL.objects.create(json=data)
    flat_data = flatten(data, separator='@')
    instance_qs = RQLJsonToSQL.objects.filter(id=instance.id)

    filter_cls = _create_filter_class(flat_data)
    filter_instance = filter_cls(queryset=instance_qs)
    _, qs = filter_instance.apply_filters(query)

    data_fits = qs.exists()
    instance_qs.delete()

    if data_fits:
        return data


def _create_filter_class(flat_data):
    filters = []
    for key, value in flat_data.items():
        # arrays are ignored for now
        if not re.search(r'@\d@', key):
            is_string = isinstance(value, str)
            if is_string:
                field_cls = models.CharField
            elif isinstance(value, int):
                field_cls = models.IntegerField
            else:
                field_cls = models.FloatField

            filters.append({
                'filter': key.replace('@', '.'),
                'source': 'json__' + key.replace('@', '__'),
                'dynamic': True,
                'field': field_cls(null=True),
                'ordering': True,
                'search': is_string,
            })

    class Cls(RQLFilterClass):
        MODEL = RQLJsonToSQL
        FILTERS = filters

    return Cls


dct = {
    'id': 'ID-123',
    'product': {
        'id': 'PRD-100-200',
    },
    'stats': {
        'versions': 3,
        'rating': 4.45,
    },
    'params': [
        {
            'id': 1,
            'value': '100',
        },
    ],
}

test_filter_by_query = partial(filter_by_query, dct)
