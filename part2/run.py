from flask import Flask
from flask_restx import Api
from config import config

# إنشاء التطبيق
app = Flask(__name__)
app.config.from_object(config['default'])
api = Api(app)

# استيراد ping
from app.api.example import ns as example_ns
api.add_namespace(example_ns)

# استيراد users
from app.api.users import ns as users_ns
api.add_namespace(users_ns, path='/api/v1/users')

# استيراد amenities
from app.api.amenities import ns as amenity_ns
api.add_namespace(amenity_ns, path='/api/v1/amenities')

# استيراد places
from app.api.places import ns as places_ns
api.add_namespace(places_ns, path='/api/v1/places')

# استيراد reviews
from app.api.reviews import ns as reviews_ns
api.add_namespace(reviews_ns, path='/api/v1/reviews')

# تشغيل التطبيق
if __name__ == "__main__":
    app.run(debug=True)
