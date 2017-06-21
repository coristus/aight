'''
Application router decoretor.

Use this to append or get rout list for specific modules.
'''

from functools import wraps

ROUTES = dict()


def blueprint_add_routes(blueprint, routes):
    '''Assign url route function configuration to given blueprint.'''
    for route in routes:
        blueprint.add_url_rule(
            route['rule'],
            endpoint=route.get('endpoint', None),
            view_func=route['view_func'],
            **route.get('options', {}))


def get_routes(module):
    '''Filter routes by given module name.'''
    if module in ROUTES.keys():
        return list(ROUTES[module])
    else:
        return ()


def application_route(rule, **kargs):
    '''Decorator function that collects application routes.'''
    def wrapper(funcion):  # pylint: disable=missing-docstring

        if funcion.__module__ not in ROUTES.keys():
            ROUTES[funcion.__module__] = []

        ROUTES[funcion.__module__].append(dict(
            rule=rule,
            view_func=funcion,
            options=kargs,
        ))

        @wraps(funcion)
        def wrapped(*args, **kwargs):  # pylint: disable=missing-docstring
            return funcion(*args, **kwargs)
        return wrapped
    return wrapper
