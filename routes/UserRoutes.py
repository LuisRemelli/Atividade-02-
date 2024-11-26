from controllers.UserController import Auth, UserGetByID, UserListAll, UserInsert, Logout, CheckIfAdmin
from flask_restful import Api


class UserRoutes:

    def __init__(self, api):
        self.api = api  # Inicializa o atributo self.api com o argumento api
        self.makeRoutes()  # Chama o método para registrar as rotas

    def makeRoutes(self):
        self.api.add_resource(UserListAll, '/usuarios')
        self.api.add_resource(UserInsert, '/register')
        self.api.add_resource(UserGetByID, '/usuarios/<string:user_id>')
        self.api.add_resource(Auth, '/login')
        self.api.add_resource(Logout, '/logout')
        self.api.add_resource(CheckIfAdmin, '/user/is-admin')