# -*- coding: utf-8 -*-
"""
`python-memcached`_ integration for Flask
==========================================

.. _python-memcached: https://pypi.python.org/pypi/python-memcached/

.. image:: https://travis-ci.org/KLab/Flask-Memcached.png
   :target: https://travis-ci.org/KLab/Flask-Memcached


Initialize
----------

::

    memcache = FlaskMemcache(app)

or::

    memcache = FlaskMemcache()
    memcache.init_app(app)


Configuration
-------------

::

    MEMCACHE = 'localhost:11211'

or::

    MEMCACHE = ['localhost:11211', 'localhost:11212']

or::

    MEMCACHE = {
        'servers': ['localhost:11211'],
        'debug': True,
        'socket_timeout': 1}

You can use different config key with `conf_key` keyword::

    session = FlaskMemcache(conf_key='MEMCACHE_SESSION')
    cache = FlaskMemcache(conf_key='MEMCACHE_CACHE')

    session.init_app(app)
    cache.init_app(app)

Limitation
----------

FlaskMemcache doesn't support multi-app setup currently.
"""
from __future__ import division, print_function, absolute_import
import memcache


class MemcacheClient(memcache.Client):
    """Wrapper for `memcache.Client`. Supports prefix."""

    def __init__(self, servers, prefix='', **kwargs):
        self.__prefix = prefix
        memcache.Client.__init__(self, servers, **kwargs)

    def _get(self, cmd, key):
        return memcache.Client._get(self, cmd, self.__prefix + key)

    def _set(self, cmd, key, val, time, min_compress_len=0):
        return memcache.Client._set(
            self, cmd, self.__prefix + key, val, time, min_compress_len)

    def get_multi(self, keys, key_prefix=''):
        return memcache.Client.get_multi(self, keys, self.__prefix + key_prefix)

    def set_multi(self, mapping, time=0, key_prefix='', min_compress_len=0):
        return memcache.Client.set_multi(self, mapping, time, self.__prefix + key_prefix,
                                         min_compress_len)

    def delete_multi(self, keys, time=0, key_prefix=''):
        return memcache.Client.delete_multi(self, keys, time, self.__prefix + key_prefix)

    get_multi.__doc__ = memcache.Client.get_multi.__doc__
    set_multi.__doc__ = memcache.Client.set_multi.__doc__
    delete_multi.__doc__ = memcache.Client.delete_multi.__doc__


class FlaskMemcache(object):
    #: :type: memcache.Client
    client = None

    def __init__(self, app=None, conf_key=None):
        self.conf_key = conf_key
        if app is not None:
            self.init_app(app, conf_key)

    def init_app(self, app, conf_key=None):
        """
        :type app: flask.Flask
        """
        conf_key = conf_key or self.conf_key or 'MEMCACHE'
        self.conf_key = conf_key
        conf = app.config[conf_key]
        if isinstance(conf, str):
            self.client = memcache.Client([conf])
        elif isinstance(conf, (list, tuple)):
            self.client = memcache.Client(conf)
        else:
            # May use 'prefix'.
            self.client = MemcacheClient(**conf)

        @app.teardown_appcontext
        def close_connection(exc=None):
            self.client.disconnect_all()
