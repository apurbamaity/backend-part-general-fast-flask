from flask_restful import Resource, reqparse
from flask import request
import os
import uuid

## query parameter -------------------------- via ?
query_perser = reqparse.RequestParser()
query_perser.add_argument("file_name", type=str, location="args")

## request body JSON ---------------------------- via requestbody

UPLOAD_FOLDER = "uploads"


class Fetchdocument(Resource):
    # def get(self, item_id):
    #     return {'message':f'okay get request working with {item_id}'}

    def __init__(self, **kwargs):
        self.db = kwargs["db"]

    def get(self):
        try:
            query_args = query_perser.parse_args()

            file_name = query_args["file_name"]
            print("file_name====>", file_name)

            if not file_name:
                return {"error": "file_name is required"}, 400

            file_path = os.path.join(UPLOAD_FOLDER, file_name)

            # ❌ File not found
            if not os.path.exists(file_path):
                return {"content": "File not found"}, 404

            # ✅ Read file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return {"file_name": file_name, "content": content}, 200

        except Exception as e:
            return e

    def post(self):
        try:
            # query_args = query_perser.parse_args()

            # item_id_q = query_args["item_id_q"]
            # item_name = query_args["item_name"]
            # return {
            #     "message": f"okay POST request working with {item_id_q} and {item_name}"
            # }

            # ✅ Get form data
            item_id_q = request.form.get("item_id_q")
            item_name = request.form.get("item_name")

            # ✅ Get file
            file = request.files.get("file")

            if file:
                # Create uploads folder if not exists
                upload_folder = "uploads"
                os.makedirs(upload_folder, exist_ok=True)

                # Avoid overwrite
                unique_name = f"{uuid.uuid4()}_{file.filename}"
                file_path = os.path.join(upload_folder, unique_name)

                file.save(file_path)
                saved_filename = unique_name

            return {
                "message": f"POST working with {item_id_q} and {item_name}",
                "saved_file": saved_filename,
            }, 200
        except Exception as e:
            return e
