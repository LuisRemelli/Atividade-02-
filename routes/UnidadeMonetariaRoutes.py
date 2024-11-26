from controllers.UnidadeMonetariaController import UnidadeMonetaria


class UnidadeMonetariaRoutes:

    def __init__(self, api):
        self.api = api  # Inicializa o atributo self.api com o argumento api
        self.makeRoutes()  # Chama o método para registrar as rotas

    def makeRoutes(self):
        self.api.add_resource(UnidadeMonetaria, '/unidades-monetarias')