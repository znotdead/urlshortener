# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['GetShortURL::test_get_url_by_code 1'] = {
    'data': {
        'exist': {
            'longUrl': 'http://localhost:8000/'
        }
    }
}

snapshots['GetShortURL::test_get_url_by_nonexists_code 1'] = {
    'data': {
        'nonexist': None
    }
}
