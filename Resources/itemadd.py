from flask_restful import Resource, reqparse
from flask import request, jsonify

from pydantic import ValidationError
from pydantic import BaseModel, EmailStr, Field  # ? probably for gt 0 like thing
from typing import List, Optional, Dict  # ?
import os
import sys

import base64, psycopg2


# Get the parent directory of this file
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add parent directory to sys.path
sys.path.append(parent_dir)
import mail

## request body JSON ---------------------------- via requestbody
body_perser = reqparse.RequestParser()
# body_perser.add_argument("data", type=list, required=True, location=["json"])
# body_perser.add_argument("created_by", type=str, required=True, location=["json"])
# body_perser.add_argument("phonenumber", type=str, required=True, location= ["json"])

body_perser.add_argument("board_data", type=list, required=True, location="json")
body_perser.add_argument("option_type", type=str, required=True)
body_perser.add_argument("created_by", type=str)


# pydantic class
class DashboardItem(BaseModel):
    dashboard_id: Optional[int] = "None"
    dashboard_name: str
    dashboard_url: Optional[str] = "None"
    dashboard_description: Optional[str] = "None"
    dashboard_icon: Optional[bytes] = "None"  # 'binary' format mapped to bytes


class ModifyDashboard(BaseModel):
    board_data: List[DashboardItem]
    option_type: str
    created_by: EmailStr


class Itemadd(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs["db"]
        self.item = Item(db=self.db)

    def get(self):
        # args = body_perser.parse_args()
        # data = args["board_data"]
        # option_type = args['option_type'] #?
        option_type = request.args.get("option_type")  # str
        created_by = request.args.get("created_by")  # str

        get_all_items = self.item.get_all()

        # Convert memoryview (BYTEA) to base64 string
        for row in get_all_items:
            for key, value in row.items():
                if isinstance(value, memoryview):
                    row[key] = base64.b64encode(value.tobytes()).decode(
                        "utf-8"
                    )  # This function decodes a Base64-encoded string (data_str) back into binary data (bytes).
        return get_all_items

    def post(self):
        """
        Get item info based on request body
        ---
        tags:
          - /itemadd (POST)
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: "#/definitions/ModifyDashboard"
        responses:
          200:
            description: Successful response
            schema:
              $ref: "#/definitions/Itempostreturn-200"
          400:
            description: bad request
            schema:
              $ref: "#/definitions/InvalidResponse"
        """

        print("here")
        # query_args = body_perser.parse_args()
        # print(f"query_args -> {query_args} ")
        # print(query_args['board_data'])

        try:
            args = body_perser.parse_args()
            """
            payload is like 
            {
            "board_data": [
                {"dashboard_id": 1, "dashboard_name": "KPI Dashboard"},
                {"dashboard_id": 2, "dashboard_name": "Sales Dashboard"}
            ],
            "option_type": "dashboard",
            "created_by": "maityapurba020@gmail.com"
            }
            """
            # args = request.get_json(force=True)

            args_pydantic = ModifyDashboard(**args)

        except ValidationError as e:
            return {"status": "error", "errors": e.errors()}

        board_data = args_pydantic.board_data
        option_type = args_pydantic.option_type
        created_by = args_pydantic.created_by

        max_dashboard_id = self.item.get_max_id()  # max_dashboard_id + 1

        items = []
        for b in board_data:

            # Convert from Pydantic model to dictionary if needed
            b_dict = b.dict() if hasattr(b, "dict") else dict(b)

            max_dashboard_id = max_dashboard_id + 1
            b_dict["dashboard_id"] = str(max_dashboard_id)

            # Add shared fields
            b_dict["option_type"] = option_type
            b_dict["created_by"] = created_by
            b_dict["dashboard_icon"] = (
                base64.b64decode(b.dashboard_icon) if b.dashboard_icon else None
            )
            items.append(b_dict)

        values = [
            (
                d["dashboard_id"],
                d["dashboard_name"],
                d["dashboard_url"],
                d["dashboard_description"],
                psycopg2.Binary(d["dashboard_icon"]),
                d["option_type"],
                d["created_by"],
            )
            for d in items
        ]

        inserted_rows = self.item.insert_many(values)

        # email_data = {"board_data": board_data, "created_by": created_by}

        # print(mail.send_mail("template.html.j2", email_data))

        return {"message": f"apurba -- with email and phone.no."}, 200


class Item:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.read_all("get_all_item.sql")

    def get_max_id(self):
        res = self.db.read_all("get_max_id.sql")
        max_dashboard_id: int = res[0].get("max") or 0
        return max_dashboard_id

    def insert_many(self, items):
        return self.db.insert_many("insert_in_item.sql", items)
