from flask import Flask
from flask_restx import Api

# إنشاء التطبيق
app = Flask(__name__)
api = Api(app)

# نستورد الـ Namespace الجاهز (مثل /ping)
from app.api.example import ns as example_ns
api.add_namespace(example_ns)

if __name__ == "__main__":
    app.run(debug=True)
