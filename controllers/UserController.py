from flask_restful import reqparse, Resource
from auth import managertk
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import json
from blacklist import BLACKLIST
from orms.user_orm import UserORM

atributosLogin = reqparse.RequestParser()
atributosLogin.add_argument('email', required=True, help="The field email cannot be left blank.")
atributosLogin.add_argument('senha', required=True, help="The field password  cannot be left blank.")

class Auth(Resource):

    def post(self):
        
        dados = atributosLogin.parse_args()
        user = UserORM.authenticate_user(dados['email'], dados['senha'])

        if user:
        
            token_de_acesso = managertk.createToken(json.dumps({"email": user["email"], "id": user["id"]}))
            
            menus = UserORM.get_menus(user["id"])
            telas = UserORM.get_telas(user["id"])
            
            return {
                "token": token_de_acesso,
                "usuario": user,
                "menus": menus,
                "telas":telas
            }
        else:
            return {"message":"E-mail ou senhas incorretos"}, 400
    
    

class UserGetByID(Resource):
    
    @jwt_required()
    def get(self, user_id):
        return {"message": 'OK'}, 200 
        # user = UserORM.getById(user_id)
        # freshAccessToken = managertk.createFreshToken()
        # user.update({"refreshToken": freshAccessToken})

        # if user["message"] == "OK":
        #     return user,200
        # else:
        #     return user, user["status_code"]
        


class Logout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.append(jwt_id)
        return {'message': 'Logged out successfully!'}, 200

class UserListAll(Resource):
    
    @jwt_required()
    def get(self):
        return {"message": 'OK'}, 200
        # user = UserORM.listAll()
        # freshAccessToken = managertk.createFreshToken()
        # user.update({"refreshToken": freshAccessToken})
        # if user["message"] == "OK":
        #     return user,200
        # else:
        #     return user, user["status_code"]
        


# atributos = reqparse.RequestParser()
# atributos.add_argument('user_name', required=True, help="The field user_name cannot be left blank.")
# atributos.add_argument('user_email', required=True, help="The field user_email cannot be left blank.")
# atributos.add_argument('user_password', required=True, help="The field user_password  cannot be left blank.")
# atributos.add_argument('user_status', required=True, help="The field user_status  cannot be left blank.")

class UserInsert(Resource):

    def post(self):
        return {"message": 'OK'}, 200
        # dados = atributos.parse_args()
        # user = UserORM.insert(dados)

        # if user:
        #     if user["message"] == "OK":
        #         return user, 200
        #     else:
        #         return user, user["status_code"]
        # return {"message":"E-mail ou senhas incorretos"}, 400