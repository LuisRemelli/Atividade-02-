from flask_restful import reqparse, Resource
from auth import managertk
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import json
from blacklist import BLACKLIST
from orms.user_orm import UserORM
from utils.logger import get_logger
from flask import request
from database.connectionDb import ConnectionDb
from orms.unidade_monetaria_orm import get_unidades_monetarias

class UnidadeMonetaria(Resource):
    
    @jwt_required()
    def get(self):
        response = get_unidades_monetarias()
        if response["message"] == "OK":
            return response, 200
        else:
            return response, response["status"]