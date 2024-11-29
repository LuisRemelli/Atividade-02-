from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import request
from utils.logger import get_logger
from orms.pessoa_orm import  insert_contato, insert_endereco, get_pessoas, get_pessoa_by_id, inserir_pessoa, update_pessoa_orm, delete_endereco_by_id, delete_contato

logger = get_logger() 


# Controller para inserir contato
class ContatoController(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            entidade_id = data.get("pessoa_entidade_id")
            tipo_contato_id = data.get("tipo_contato_id")
            contato = data.get("contato")

            if not entidade_id or not tipo_contato_id or not contato:
                return {"message": "Parâmetros insuficientes", "status": 400}, 400

            response = insert_contato(entidade_id, tipo_contato_id, contato)
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao inserir contato: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para inserir endereço
class EnderecoController(Resource):
    @jwt_required()
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("entidade_id", type=int, required=True, help="ID da entidade é obrigatório")
            parser.add_argument("tipo_endereco_id", type=int, required=True, help="ID do tipo de endereço é obrigatório")
            parser.add_argument("cidade_id", type=int, required=True, help="ID da cidade é obrigatório")
            parser.add_argument("cep", type=str, required=True, help="CEP é obrigatório")
            parser.add_argument("logradouro", type=str, required=True, help="Logradouro é obrigatório")
            parser.add_argument("numero", type=str, required=True, help="Número é obrigatório")
            parser.add_argument("bairro", type=str, required=True, help="Bairro é obrigatório")
            parser.add_argument("complemento", type=str, required=False)

            args = parser.parse_args()

            if len(args["cep"]) > 8 or len(args["numero"]) > 8:
                return {"message": "CEP ou número inválido (máximo 8 caracteres)", "status": 400}, 400

            response = insert_endereco(
                args["entidade_id"],
                args["tipo_endereco_id"],
                args["cidade_id"],
                args["cep"],
                args["logradouro"],
                args["numero"],
                args["bairro"],
                args.get("complemento"),
            )

            return response, response.get("status", 500)
        except Exception as e:
            logger.error(f"Erro ao inserir endereço: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para listar pessoas
class ListarPessoasController(Resource):
    @jwt_required()
    def get(self):
        try:
            response = get_pessoas()
            return response, response.get("status", 500)
        except Exception as e:
            logger.error(f"Erro ao listar pessoas: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para listar pessoa por ID
class ListarPessoaPorIdController(Resource):
    @jwt_required()
    def get(self, pessoa_id):
        try:
            response = get_pessoa_by_id(pessoa_id)
            if response.get("status") == 404:
                return {"message": "Pessoa não encontrada", "status": 404}, 404
            return response, 200
        except Exception as e:
            logger.error(f"Erro ao buscar pessoa por ID: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para criar pessoa
class CriarPessoaController(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument("nome", required=False, help="O campo 'nome' pode ser preenchido.")
    atributos.add_argument("cpf", required=False, help="O campo 'cpf' pode ser preenchido.")
    atributos.add_argument("ativo", required=True, help="O campo 'ativo' não pode ficar em branco.")
    atributos.add_argument("data_nascimento", required=True, help="O campo 'data_nascimento' não pode ficar em branco.")

    @jwt_required()
    def post(self):
        try:
            pessoa = self.atributos.parse_args()

            if not pessoa.get("nome") or not pessoa.get("cpf"):
                return {"message": "Os campos 'nome' e 'cpf' são obrigatórios.", "status": 400}, 400

            cpf = pessoa.get("cpf")
            if not cpf.isdigit() or len(cpf) != 11:
                return {"message": "Digite um número de CPF válido.", "status": 400}, 400

            response = inserir_pessoa(pessoa)
            return response, response.get("status", 500)
        except Exception as e:
            logger.error(f"Erro ao criar pessoa: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para atualizar pessoa
class PessoaUpdateController(Resource):
    @jwt_required()
    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("id", type=int, required=True, help="O ID da pessoa é obrigatório.")
            parser.add_argument("nome", type=str, required=True, help="O nome da pessoa é obrigatório.")
            parser.add_argument("cpf", type=str, required=True, help="O CPF é obrigatório.")
            parser.add_argument("data_nascimento", type=str, required=True, help="A data de nascimento é obrigatória.")
            parser.add_argument("ativo", type=bool, required=True, help="O status ativo é obrigatório.")

            args = parser.parse_args()

            response = update_pessoa_orm(
                id=args["id"],
                nome=args["nome"],
                cpf=args["cpf"],
                data_nascimento=args["data_nascimento"],
                ativo=args["ativo"],
            )

            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao atualizar pessoa: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para remover endereço
class RemoverEnderecoController(Resource):
    @jwt_required()
    def delete(self, endereco_id):
        try:
            logger.info(f"Tentando excluir endereço com ID {endereco_id}")
            response = delete_endereco_by_id(endereco_id)
            if response.get("status") == 404:
                return {"message": "Endereço não encontrado", "status": 404}, 404
            return response, 200
        except Exception as e:
            logger.error(f"Erro ao remover endereço: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500


# Controller para remover contato com ID na URL
class DeleteContatoController(Resource):
    @jwt_required()
    def delete(self, contato_id):
        try:
            if not contato_id:
                return {"message": "Parâmetro 'contato_id' é obrigatório", "status": 400}, 400

            response = delete_contato(contato_id)
            return response, response.get("status", 400)
        except Exception as e:
            logger.error(f"Erro ao remover contato: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500