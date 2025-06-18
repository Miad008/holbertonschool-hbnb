from flask_restx import Namespace, Resource

ns = Namespace('users', description='Test user namespace')

@ns.route('/')
class UserList(Resource):
    def get(self):
        return {"message": "Hello from users!"}
