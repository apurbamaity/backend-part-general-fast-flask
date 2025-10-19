from flask_restful import Resource, reqparse

## query parameter -------------------------- via ?
query_perser = reqparse.RequestParser()
query_perser.add_argument("item_id_q", type=str, location="args")
query_perser.add_argument("item_name", type=str, location="args")

## request body JSON ---------------------------- via requestbody


class Item(Resource):
    # def get(self, item_id):
    #     return {'message':f'okay get request working with {item_id}'}

    def __init__(self, **kwargs):
        self.db = kwargs["db"]

    def get(self):
        """
        Get item info based on query parameters
        ---
        tags:
          - /item (GET)
        parameters:
          - name: item_id_q
            in: query
            type: string
            required: true
            description: The item ID query parameter
          - name: item_name
            in: query
            type: string
            required: true
            description: The item name
        responses:
          200:
            description: Successful response
            schema:
              $ref: "#/definitions/Itemget"
        """
        try:
            query_args = query_perser.parse_args()

            item_id_q = query_args["item_id_q"]
            item_name = query_args["item_name"]
            return {
                "message": f"okay get request working with {item_id_q} and {item_name}"
            }

        except Exception as e:
            return e

    def post(self):
        try:
            query_args = query_perser.parse_args()

            item_id_q = query_args["item_id_q"]
            item_name = query_args["item_name"]
            return {
                "message": f"okay POST request working with {item_id_q} and {item_name}"
            }

        except Exception as e:
            return e
