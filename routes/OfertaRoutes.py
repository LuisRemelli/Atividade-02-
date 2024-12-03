from controllers.OfertaController import OfertaController

class OfertaRoutes:
    def __init__(self, api):
        self.api = api
        self.make_routes()

    def make_routes(self):
        self.api.add_resource(OfertaController, "/oferta/criar/oferta")
