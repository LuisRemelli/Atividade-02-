from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import request
from utils.logger import get_logger
from orms.oferta_orm import insert_oferta

# Inicializa o logger
logger = get_logger()

class OfertaController(Resource):
    @jwt_required()
    def post(self):
        """
        Criação de uma nova oferta com dados obrigatórios e opcionais.
        """
        try:
            # Recebe os dados do corpo da requisição
            data = request.get_json()

            # Valida o campo obrigatório `entidade_id`
            entidade_id = data.get("entidade_id")
            if not entidade_id:
                return {"message": "O campo 'entidade_id' é obrigatório.", "status": 400}, 400

            # Dados opcionais
            endereco = data.get("endereco")  # Endereço associado à oferta
            produtos = data.get("produtos")  # Produtos associados à oferta
            contatos = data.get("contatos")  # Contatos associados à oferta
            bids = data.get("bids")          # Bids associados à oferta

            # Chamando a função de ORM para criar a oferta
            response = insert_oferta(
                entidade_id=entidade_id,
                endereco=endereco,
                produtos=produtos,
                contatos=contatos,
                bids=bids
            )

            # Retorna a resposta com o status apropriado
            return response, response.get("status", 500)

        except Exception as e:
            # Log do erro para depuração
            logger.error(f"Erro ao criar oferta: {str(e)}")
            return {"message": "Erro interno no servidor", "status": 500}, 500
