from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import request
from utils.logger import get_logger
from orms.produto_orm import inserir_produto, listar_produtos, atualizar_produto, inserir_safra, listar_safras, atualizar_safra, relacionar_produto_safra, remover_relacao_produto_safra

logger = get_logger()

# Controller para inserir um produto
class InserirProdutoController(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
            parser.add_argument("sigla", type=str, required=True, help="O campo 'sigla' é obrigatório.")
            args = parser.parse_args()

            if len(args["sigla"]) > 5:
                return {"message": "Sigla deve ter no máximo 5 caracteres", "status": 400}, 400

            response = inserir_produto(args["nome"], args["sigla"])
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao inserir produto: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500

# Controller para listar produtos
class ListarProdutosController(Resource):
    @jwt_required()
    def get(self):
        try:
            response = listar_produtos()
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao listar produtos: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500

# Controller para atualizar um produto
class AtualizarProdutoController(Resource):
    @jwt_required()
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type=int, required=True, help="O ID do produto é obrigatório.")
            parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
            parser.add_argument("sigla", type=str, required=True, help="O campo 'sigla' é obrigatório.")
            args = parser.parse_args()

            response = atualizar_produto(args["id"], args["nome"], args["sigla"])
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao atualizar produto: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500
        
        
# Controller para inserir uma safra
class InserirSafraController(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
            parser.add_argument("sigla", type=str, required=True, help="O campo 'sigla' é obrigatório.")
            args = parser.parse_args()

            if len(args["sigla"]) > 5:
                return {"message": "Sigla deve ter no máximo 5 caracteres", "status": 400}, 400

            response = inserir_safra(args["nome"], args["sigla"])
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao inserir safra: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para listar safras
class ListarSafrasController(Resource):
    @jwt_required()
    def get(self):
        try:
            response = listar_safras()
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao listar safras: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500



class AtualizarSafraController(Resource):
    @jwt_required()
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type=int, required=True, help="O ID da safra é obrigatório.")
            parser.add_argument("nome", type=str, required=True, help="O campo 'nome' é obrigatório.")
            parser.add_argument("sigla", type=str, required=True, help="O campo 'sigla' é obrigatório.")
            args = parser.parse_args()

            response = atualizar_safra(args["id"], args["nome"], args["sigla"])
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao atualizar safra: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500

# Controller para relacionar um produto com uma safra
class RelacionarProdutoSafraController(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("entidade_id", type=int, required=True, help="O ID do produto é obrigatório e deve ser um inteiro.")
            parser.add_argument("safra_id", type=int, required=True, help="O ID da safra é obrigatório e deve ser um inteiro.")
            args = parser.parse_args()

            logger.debug(f"Argumentos recebidos: {args}")
            response = relacionar_produto_safra(args["entidade_id"], args["safra_id"])
            if response.get("status") == 201:
                logger.info(f"Produto ID {args['entidade_id']} relacionado com Safra ID {args['safra_id']}")
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao relacionar produto com safra: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500, "error": str(e)}, 500

# Controller para remover a relação entre um produto e uma safra
class RemoverRelacaoProdutoSafraController(Resource):
    @jwt_required()
    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("entidade_id", type=int, required=True, help="O ID do produto é obrigatório e deve ser um inteiro.")
            parser.add_argument("safra_id", type=int, required=True, help="O ID da safra é obrigatório e deve ser um inteiro.")
            args = parser.parse_args()

            logger.debug(f"Argumentos recebidos: {args}")
            response = remover_relacao_produto_safra(args["entidade_id"], args["safra_id"])
            if response.get("status") == 200:
                logger.info(f"Relação entre Produto ID {args['entidade_id']} e Safra ID {args['safra_id']} removida com sucesso")
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao remover relação entre produto e safra: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500, "error": str(e)}, 500