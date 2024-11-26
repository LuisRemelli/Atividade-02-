from controllers.UnidadeDeMedidaController import UnidadeDeMedida

class UnidadeDeMedidaRoutes:

    def __init__(self, api):
        self.api = api
        self.makeRoutes()

    def makeRoutes(self):
        self.api.add_resource(UnidadeDeMedida, '/unidades-medida')
