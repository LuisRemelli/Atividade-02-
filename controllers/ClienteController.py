from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import request
from utils.logger import get_logger
from orms.cliente_orm import insert_cliente, update_cliente, get_clientes, insert_cliente_contato, validate_entidade_id

logger = get_logger()


# Controller para inserir cliente
class ClienteInsertController(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("grupo_producao_entidade_id", type=int, required=True, help="Grupo produção é obrigatório")
            parser.add_argument("tipo_pessoa", type=str, required=True, help="Tipo pessoa é obrigatório")
            parser.add_argument("razao_social", type=str, required=True, help="Razão social é obrigatória")
            parser.add_argument("nome_fantasia", type=str, required=True, help="Nome fantasia é obrigatório")
            parser.add_argument("documento", type=str, required=True, help="Documento é obrigatório")
            parser.add_argument("matriz", type=bool, required=True, help="Campo matriz é obrigatório")

            args = parser.parse_args()
            response = insert_cliente(
                args["grupo_producao_entidade_id"],
                args["tipo_pessoa"],
                args["razao_social"],
                args["nome_fantasia"],
                args["documento"],
                args["matriz"]
            )
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao inserir cliente: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para atualizar cliente
class ClienteUpdateController(Resource):
    @jwt_required()
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type=int, required=True, help="ID do cliente é obrigatório")
            parser.add_argument("grupo_producao_entidade_id", type=int, required=True, help="Grupo produção é obrigatório")
            parser.add_argument("tipo_pessoa", type=str, required=True, help="Tipo pessoa é obrigatório")
            parser.add_argument("razao_social", type=str, required=True, help="Razão social é obrigatória")
            parser.add_argument("nome_fantasia", type=str, required=True, help="Nome fantasia é obrigatório")
            parser.add_argument("documento", type=str, required=True, help="Documento é obrigatório")
            parser.add_argument("matriz", type=bool, required=True, help="Campo matriz é obrigatório")

            args = parser.parse_args()
            response = update_cliente(
                args["id"],
                args["grupo_producao_entidade_id"],
                args["tipo_pessoa"],
                args["razao_social"],
                args["nome_fantasia"],
                args["documento"],
                args["matriz"]
            )
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao atualizar cliente: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para listar clientes
class ClienteListController(Resource):
    @jwt_required()
    def get(self):
        try:
            response = get_clientes()
            return response, response.get("status", 500)
        except Exception as e:
            logger.error(f"Erro ao listar clientes: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para inserir contato de cliente
class ClienteContatoInsertController(Resource):
    @jwt_required()
    def post(self):
        try:
            # Definição dos argumentos esperados na requisição
            parser = reqparse.RequestParser()
            parser.add_argument("entidade_id", type=int, required=True, help="ID da entidade é obrigatório")
            parser.add_argument("pessoa_entidade_id", type=int, required=True, help="ID da pessoa é obrigatório")
            args = parser.parse_args()

            if not validate_entidade_id(args["entidade_id"]):
                return {"message": "Entidade não encontrada", "status": 400}, 400
            

            response = insert_cliente_contato(args["entidade_id"], args["pessoa_entidade_id"])
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao inserir contato de cliente: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500
