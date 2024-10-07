from controllers.UserController import Auth, UserGetByID, UserListAll, UserInsert, Logout

class UserRoutes:

    def __init__(self, api):
        self.api = api
        self.makeRoutes()
    
    def makeRoutes(self):
        self.api.add_resource(UserListAll, '/usuarios')
        self.api.add_resource(UserInsert, '/register')
        self.api.add_resource(UserGetByID, '/usuarios/<string:user_id>')
        self.api.add_resource(Auth, '/login')
        self.api.add_resource(Logout, '/logout')