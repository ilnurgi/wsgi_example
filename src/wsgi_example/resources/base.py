# coding: utf-8


class ResourceExtension(object):
    """Скопировано прямо из новы, либерти
    класс. описывает ресур для регистрации в нове
    """

    def __init__(self, collection, controller=None, parent=None,
                 collection_actions=None, member_actions=None,
                 custom_routes_fn=None, inherits=None, member_name=None):
        if not collection_actions:
            collection_actions = {}
        if not member_actions:
            member_actions = {}
        self.collection = collection
        self.controller = controller
        self.parent = parent
        self.collection_actions = collection_actions
        self.member_actions = member_actions
        self.custom_routes_fn = custom_routes_fn
        self.inherits = inherits
        self.member_name = member_name


class Resource(object):
    """
    Данный ресурс управляет выбором экшенов в контроллере, при обработке запроса
    """

    def __init__(self, controller):
        self.controller = controller

    def __call__(self, environ, start_response):
        action = environ['wsgiorg.routing_args'][1]['action']
        method = self.get_action(action)
        if not method:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ['404, Resource not have action "{0}"'.format(action)]
        return method(environ, start_response)

    def get_action(self, action):
        return getattr(self.controller, action, None)

