from flask_restful import Resource, reqparse
from flask import request
import os
import uuid

## query parameter -------------------------- via ?
query_perser = reqparse.RequestParser()
query_perser.add_argument("user_query", type=str, location="args")

## request body JSON ---------------------------- via requestbody

UPLOAD_FOLDER = "uploads"


class ASkquestion(Resource):
    # def get(self, item_id):
    #     return {'message':f'okay get request working with {item_id}'}

    def __init__(self, **kwargs):
        self.db = kwargs["db"]

    def get(self):
        try:
            query_args = query_perser.parse_args()

            user_query = query_args["user_query"]
            print("user_query====>", user_query)

            if not user_query:
                return {"error": "file_name is required"}, 400

            #     file_path = os.path.join(UPLOAD_FOLDER, file_name)

            #     # ❌ File not found
            #     if not os.path.exists(file_path):
            #         return {"error": "File not found"}, 404

            #     # ✅ Read file
            #     with open(file_path, "r", encoding="utf-8") as f:
            #         content = f.read()

            return {"answer": "hello from bot"}, 200

        except Exception as e:
            return e
