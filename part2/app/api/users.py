from flask import request
from flask_restx import Namespace, Resource, fields
from app.core.facade import HBnBFacade

# إنشاء واجهة API للمستخدمين
ns = Namespace('users', description='User operations')
facade = HBnBFacade()

# نموذج بيانات المستخدم (للتوثيق والاختبار)
user_model = ns.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
})

@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        """استعراض كل المستخدمين"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users]

    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """إنشاء مستخدم جديد"""
        user_data = request.json
        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

@ns.route('/<string:user_id>')
@ns.param('user_id', 'The User identifier')
class UserResource(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """استعراض مستخدم حسب ID"""
        user = facade.get_user(user_id)
        if user:
            return user.to_dict()
        ns.abort(404, f"User with id {user_id} not found.")

    def delete(self, user_id):
        """حذف مستخدم"""
        deleted = facade.delete_user(user_id)
        if deleted:
            return {"message": f"User {user_id} deleted."}
        ns.abort(404, f"User with id {user_id} not found.")
        
