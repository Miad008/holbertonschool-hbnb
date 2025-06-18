from flask_restx import Namespace, Resource

# تعريف الـ namespace
ns = Namespace('users', description='Test User Namespace')

# نقطة وصول تجريبية
@ns.route('/')
class UserList(Resource):
    def get(self):
        return {"message": "Users API is working!"}
