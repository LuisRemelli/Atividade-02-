from controllers.GrupoProducaoController import (
    InserirGrupoProducaoController,
    ListarGruposProducaoController,
    ListarGrupoPorIdController,
    AtualizarGrupoProducaoController,
)

class GrupoProducaoRoutes:
    def __init__(self, api):
        self.api = api
        self.make_routes()

    def make_routes(self):
        self.api.add_resource(InserirGrupoProducaoController, "/grupo-producao/inserir")
        self.api.add_resource(ListarGruposProducaoController, "/grupo-producao/listar")
        self.api.add_resource(ListarGrupoPorIdController, "/grupo-producao/listar/<int:grupo_id>")
        self.api.add_resource(AtualizarGrupoProducaoController, "/grupo-producao/atualizar/<int:grupo_id>")
