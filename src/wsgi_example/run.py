# coding: utf-8

from wsgiref import simple_server

from routes import Mapper
from routes.middleware import RoutesMiddleware

from resources.base import Resource
from resources.hypervisors import HypervisorsExtension


class Application(object):

    def __init__(self):
        self.mapper = self.get_mapper()
        self._router = RoutesMiddleware(
            wsgi_app=self._dispatch, mapper=self.mapper)

    def __call__(self, environ, start_response):
        resource = self._router(environ, start_response)
        if not resource:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return ['404, Resource not found']
        return resource(environ, start_response)

    @staticmethod
    def _dispatch(environ, start_response):
        url, match = environ.get('wsgiorg.routing_args', (None, None))
        if match:
            controller = match['controller']
        else:
            controller = None
        return controller

    def get_mapper(self):
        mapper = Mapper()
        self.register_resources(mapper)
        return mapper

    def register_resources(self, mapper):
        for ext in (HypervisorsExtension(), ):
            resources = ext.get_resources()
            for res in resources:
                mapper.resource(
                    res.collection,
                    res.collection,
                    controller=Resource(res.controller),
                    collection=res.collection_actions,
                    member=res.member_actions)


app = Application()

server = simple_server.make_server('', 8003, app)
server.serve_forever()
