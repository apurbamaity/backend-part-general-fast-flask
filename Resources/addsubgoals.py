from flask import request
from flask_restful import Resource, reqparse

## query parameter -------------------------- via ?
query_perser = reqparse.RequestParser()
query_perser.add_argument("subgoals", type=[], required=True, location="json")

## request body JSON ---------------------------- via requestbody


class Addsubgoals(Resource):

    def __init__(self, **kwargs):
        self.db = kwargs["db"]
        self.goal = Goal(kwargs["db"])

    def post(self):
        try:
            print("[1] -> within /subgoals POST method")
            query_args = request.get_json()
            print(f"[1.i] -> query_args = {query_args} | {type(query_args)}")
            subgoals_list = query_args["subgoals"]
            print(
                f"[1.ii] -> subgoals_list = {subgoals_list} | {type(subgoals_list)} {type(subgoals_list[0])}"
            )

            return self.goal.addsubgoals(2, subgoals_list)

        except Exception as e:
            return e

    def get(self):
        return self.goal.get_all()


class Goal:
    def __init__(self, db):
        self.db = db

    def addsubgoals(self, goal_id, subgoals):
        goals_and_subgoals = []
        for sg in subgoals:
            goals_and_subgoals.append((goal_id, sg))
        print(f"[1.iii] -> goals_and_subgoals = {goals_and_subgoals}")
        return self.db.insert_many("inser_many_subgoals.sql", goals_and_subgoals)

    def get_all(self):
        return self.db.read_all("get_all_goals.sql")
