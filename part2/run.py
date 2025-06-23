from flask import Flask
from flask_restx import Api

# إنشاء التطبيق
app = Flask(__name__)
api = Api(app)

# استيراد ping
from app.api.example import ns as example_ns
api.add_namespace(example_ns)

# استيراد users
from app.api.users import ns as users_ns
api.add_namespace(users_ns)

from app.amenities import ns as amenity_ns
pi.add_namespace(amenity_ns)

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
