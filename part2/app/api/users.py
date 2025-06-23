from flask import request
from flask_restx import Namespace, Resource, fields
from app.core.facade import HBnBFacade

# إنشاء واجهة API للمستخدمين
ns = Namespace('users', description='User operations')
facade = HBnBFacade()

# نموذج بيانات المستخدم (بدون كلمة المرور كما هو مطلوب)
user_model = ns.model('User', {
    'first_name': fields.String(required=True, description="User's first name"),
    'last_name': fields.String(required=True, description="User's last name"),
    'email': fields.String(required=True, description="User's email address"),
})

@ns.route('/')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        """عرض جميع المستخدمين (GET /users)"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users]

    @ns.expect(user_model)
    @ns.response(201, 'User created successfully')
    def post(self):
        """إنشاء مستخدم جديد (POST /users)"""
        user_data = request.json
        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

@ns.route('/<string:user_id>')
@ns.param('user_id', 'معرّف المستخدم')
class UserItem(Resource):
    @ns.marshal_with(user_model)
    def get(self, user_id):
        """عرض مستخدم حسب المعرّف (GET /users/<id>)"""
        user = facade.get_user(user_id)
        if not user:
            ns.abort(404, "المستخدم غير موجود")
        return user.to_dict()

    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    def put(self, user_id):
        """تحديث بيانات مستخدم (PUT /users/<id>)"""
        user_data = request.json
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            ns.abort(404, "المستخدم غير موجود")
        return updated_user.to_dict()

    ##def delete(self, user_id):
    #    """حذف مستخدم"""
     #   deleted = facade.delete_user(user_id)
      #  if deleted:
       #     return {"message": f"User {user_id} deleted."}
        #ns.abort(404, f"User with id {user_id} not found.")
