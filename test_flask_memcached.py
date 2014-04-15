# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import memcache
import flask.ext.memcached


def test_simple():
    mc = memcache.Client(['localhost:11211'])
    memcached = flask.ext.memcached.FlaskMemcache()
    app = flask.Flask(__name__)
    app.config['MEMCACHE'] = {
        'servers': ['localhost:11211'],
        'prefix': b'px',
    }
    memcached.init_app(app)

    with app.app_context():
        memcached.client.set(b'foo', b'bar')
        assert memcache.client.get(b'foo') == b'bar'

    assert mc.get(b'pxfoo') == b'bar'
