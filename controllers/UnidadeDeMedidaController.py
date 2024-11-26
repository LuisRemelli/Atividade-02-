from flask_restful import Resource
from flask_jwt_extended import jwt_required
from database.connectionDb import ConnectionDb
from orms.unidade_medida_orm import get_unidades_medida

class UnidadeDeMedida(Resource):

    @jwt_required()
    def get(self):
        response = get_unidades_medida()
        if response["message"] == "OK":
            return response, 200
        else:
            return response, response["status"]
