# coding: utf-8

"""
пример ресурса
"""

from resources.base import ResourceExtension


class HypervisorsController(object):
    """
    контроллер
    """

    def index(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return ['Hello Hypervisors']


class HypervisorsExtension(object):
    """
    расширение ресурсов для новы
    """

    def get_resources(self):
        return [
            ResourceExtension(
                'hypervisors',
                member_name='hypervisor',
                controller=HypervisorsController(),
                collection_actions={
                    'count': 'GET'
                },
                member_actions={
                    'is_available': 'GET',
                    'action': 'POST'
                },
                parent=None,
                custom_routes_fn=None,
                inherits=None
            )
        ]
