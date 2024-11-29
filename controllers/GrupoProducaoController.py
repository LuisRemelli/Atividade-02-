from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from orms.grupo_producao_orm import (
    inserir_grupo_producao,
    listar_grupos_producao,
    listar_grupo_por_id,
    atualizar_grupo_producao,
)

class InserirGrupoProducaoController(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
        parser.add_argument("ativo", type=bool, required=True, help="O campo 'ativo' é obrigatório.")
        args = parser.parse_args()

        response = inserir_grupo_producao(args["nome"], args["ativo"])
        return response, response.get("status", 400)


class ListarGruposProducaoController(Resource):
    @jwt_required()
    def get(self):
        response = listar_grupos_producao()
        return response, response.get("status", 400)


class ListarGrupoPorIdController(Resource):
    @jwt_required()
    def get(self, grupo_id):
        response = listar_grupo_por_id(grupo_id)
        return response, response.get("status", 400)


class AtualizarGrupoProducaoController(Resource):
    @jwt_required()
    def put(self, grupo_id):
        parser = reqparse.RequestParser()
        parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
        parser.add_argument("ativo", type=bool, required=True, help="O campo 'ativo' é obrigatório.")
        args = parser.parse_args()

        response = atualizar_grupo_producao(grupo_id, args["nome"], args["ativo"])
        return response, response.get("status", 400)
