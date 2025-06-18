from flask_restx import Namespace, Resource

ns = Namespace('users', description='Test user namespace')

@ns.route('/')
class TestUser(Resource):
    def get(self):
        return {"message": "User API works!"}
