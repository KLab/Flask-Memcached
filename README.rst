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

Flask-Memcached doesn't support multi-app setup currently.
