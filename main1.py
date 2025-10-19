from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
import json


from Resources.item import Item
from Resources.itemadd import Itemadd
from Resources.addsubgoals import Addsubgoals


# swagger
from flasgger import Swagger
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

# database
from database import Database


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})
api = Api(app)

# Initialize DB
db = Database(app)


api.add_resource(Item, "/item", resource_class_kwargs={"db": db})
api.add_resource(Itemadd, "/item_add", resource_class_kwargs={"db": db})
api.add_resource(Addsubgoals, "/subgoals", resource_class_kwargs={"db": db})


# Swagger JSON route
@app.route("/swagger")
def get_swagger():
    swag = swagger(app)
    swag["info"]["version"] = "1.0"
    swag["info"]["title"] = "My API Documentation"
    # Load your schemas if you have any
    with open("schemas.json", "r") as f:
        swag["definitions"] = json.load(f)
    return jsonify(swag)


# Swagger UI route
SWAGGER_URL = "/swagger-ui"
API_URL = "/swagger"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "My API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/")
def home():
    return "<h1>hello world</h1>"


if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from flask_restful import Api, Resource
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"*": {"origins": "http://localhost:5173"}})
# api = Api(app)


# class Item(Resource):
#     def get(self):
#         print("here it comes")
#         return {"message": "Hello from Item"}

#     def post(self):
#         data = request.get_json()
#         # handle data
#         return {"received": data}, 201


# api.add_resource(Item, "/item")

# if __name__ == "__main__":
#     app.run(debug=True)
