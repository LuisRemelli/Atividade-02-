from controllers.PessoaController import (
    ContatoController,
    EnderecoController,
    ListarPessoasController,
    ListarPessoaPorIdController,
    CriarPessoaController,
    PessoaUpdateController,
    RemoverEnderecoController,
    DeleteContatoController,
)

class PessoaRoutes:
    def __init__(self, api):
        self.api = api
        self.make_routes()

    def make_routes(self):
        self.api.add_resource(ContatoController, "/pessoa/inserir/contato") # URL para inserir contato 
        self.api.add_resource(EnderecoController, "/pessoa/inserir/endereco") # URL para inserir endereço
        self.api.add_resource(ListarPessoasController, "/pessoa/listar/pessoas") # URL para listar pessoa
        self.api.add_resource(ListarPessoaPorIdController, "/pessoa/listar/pessoa/<int:pessoa_id>") # URL para listar pessoa por ID
        self.api.add_resource(CriarPessoaController, "/pessoa/inserir/pessoa") # URL para inserir pessoa
        self.api.add_resource(PessoaUpdateController, "/pessoa/atualizar/pessoa") # URL para atualizar pessoa
        self.api.add_resource(RemoverEnderecoController, "/pessoa/remover/endereco/<int:endereco_id>") # URL para remover endereço por ID
        self.api.add_resource(DeleteContatoController, "/pessoa/remover/contato/<int:contato_id>") # URL para remover contato por ID
