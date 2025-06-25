from flask_restx import Namespace, Resource

ns = Namespace('ping', description='Ping test namespace')

@ns.route('/')
class PingResource(Resource):
    def get(self):
        return {"message": "pong!"}
