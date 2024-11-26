from flask_restful import Resource


class _Start(Resource):
    def get(self):
          return {
            "title": "Agrinvest ACB API",
            "description": "API para o sistema ACB da Agrinvest.",
            "author": "SantoroIN",
            "version": "1.0.0",
            }, 200

class StartRoute:

    def __init__(self, api):
        self.api = api
        self.makeRoutes()

    def makeRoutes(self):
        self.api.add_resource(_Start, '/')
