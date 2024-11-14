from flask_restful import reqparse, Resource
from auth import managertk
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import json
from blacklist import BLACKLIST
from orms.user_orm import UserORM
from utils.logger import get_logger
from flask import request

# Configuração do logger
logger = get_logger()

atributosLogin = reqparse.RequestParser()
atributosLogin.add_argument('email', required=True, help="O campo email não pode ficar em branco.")
atributosLogin.add_argument('senha', required=True, help="O campo senha não pode ficar em branco.")

class Auth(Resource):

    def post(self):
        dados = atributosLogin.parse_args()
        user = UserORM.authenticate_user(dados['email'], dados['senha'])

        if user:
            # Captura o IP e o User-Agent do cliente
            client_ip = request.remote_addr
            user_agent = request.headers.get("User-Agent", "User-Agent não encontrado")

            # Loga os detalhes do login
            logger.info(f"Login realizado com sucesso - ID: {user['id']}, IP: {client_ip}, User-Agent: {user_agent}, Usuário: {dados['email']}")

            # Registra o login no banco de dados
            UserORM.insert_login_log(user["id"], client_ip, user_agent)

            # Geração do token de acesso
            token_de_acesso = managertk.createToken(json.dumps({"email": user["email"], "id": user["id"]}))
            
            # Obtém menus e telas do usuário
            menus = UserORM.get_menus(user["id"])
            telas = UserORM.get_telas(user["id"])
            
            return {
                "token": token_de_acesso,
                "usuario": user,
                "menus": menus,
                "telas": telas
            }
        else:
            # Loga tentativa de login com falha
            client_ip = request.remote_addr
            user_agent = request.headers.get("User-Agent", "User-Agent não encontrado")
            logger.warning(f"Tentativa de login falhou para o usuário: {dados['email']} - IP: {client_ip}, User-Agent: {user_agent}")
            
            return {"message": "E-mail ou senha incorretos"}, 400
    

class UserGetByID(Resource):
    
    @jwt_required()
    def get(self, user_id):
        # Obtém o usuário pelo ID
        user = UserORM.getById(user_id)
        freshAccessToken = managertk.createFreshToken()
        user.update({"refreshToken": freshAccessToken})

        if user["message"] == "OK":
            return user, 200
        else:
            return user, user["status_code"]


class Logout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] 
        BLACKLIST.append(jwt_id)
        return {'message': 'Logged out successfully!'}, 200

class UserListAll(Resource):
    
    @jwt_required()
    def get(self):
        # Lista todos os usuários
        user = UserORM.listAll()
        freshAccessToken = managertk.createFreshToken()
        user.update({"refreshToken": freshAccessToken})
        if user["message"] == "OK":
            return user, 200
        else:
            return user, user["status_code"]

atributos = reqparse.RequestParser()
atributos.add_argument('user_name', required=True, help="O campo user_name não pode ficar em branco.")
atributos.add_argument('user_email', required=True, help="O campo user_email não pode ficar em branco.")
atributos.add_argument('user_password', required=True, help="O campo user_password não pode ficar em branco.")
atributos.add_argument('user_status', required=True, help="O campo user_status não pode ficar em branco.")

class UserInsert(Resource):

    def post(self):
        dados = atributos.parse_args()
        user = UserORM.insert(dados)

        if user:
            if user["message"] == "OK":
                return user, 200
            else:
                return user, user["status_code"]
        return {"message": "E-mail ou senha incorretos"}, 400
