from controllers.ProdutoController import (
    InserirProdutoController,
    ListarProdutosController,
    AtualizarProdutoController,
    InserirSafraController,
    ListarSafrasController,
    AtualizarSafraController,
)

class ProdutoRoutes:
    def __init__(self, api):
        self.api = api
        self.make_routes()

    def make_routes(self):
        self.api.add_resource(InserirProdutoController, "/produto/inserir/produto") # URL para inserir produto
        self.api.add_resource(ListarProdutosController, "/produto/listar/produtos") # URL para listar produtos
        self.api.add_resource(AtualizarProdutoController, "/produto/atualizar/produto") # URL para atualizar produtos
        self.api.add_resource(InserirSafraController, "/produto/inserir/safra") # URL para inserir safra
        self.api.add_resource(ListarSafrasController, "/produto/listar/safras") # URL para listar safra
        self.api.add_resource(AtualizarSafraController, "/produto/atualizar/safra") # URL para atualizar safra 
