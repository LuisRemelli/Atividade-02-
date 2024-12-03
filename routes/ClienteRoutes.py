from controllers.ClienteController import (
    ClienteInsertController,
    ClienteUpdateController,
    ClienteListController,
    ClienteContatoInsertController,
)


class ClienteRoutes:
    def __init__(self, api):
        self.api = api
        self.make_routes()

    def make_routes(self):
        self.api.add_resource(ClienteInsertController, "/cliente/inserir")
        self.api.add_resource(ClienteUpdateController, "/cliente/atualizar")
        self.api.add_resource(ClienteListController, "/cliente/listar")
        self.api.add_resource(ClienteContatoInsertController, "/cliente/inserir/contato")
