from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
import psycopg2

app = Flask(__name__)
api = Api(app)

conn = psycopg2.connect(host=host, database=database, user=user, password=password)
curs = conn.cursor()

post_parser = reqparse.RequestParser()
post_parser.add_argument("name", type=str, help="Name is required.", required=True)
post_parser.add_argument("address", type=str)
post_parser.add_argument("ssn", type=int)
post_parser.add_argument("college", type=str)

patch_parser = reqparse.RequestParser()
patch_parser.add_argument("name", type=str)
patch_parser.add_argument("address", type=str)
patch_parser.add_argument("ssn", type=int)
patch_parser.add_argument("college", type=str)


def search_id(arr, low, high, target):
    if high >= low:
        m = (low + high) // 2
        if arr[m][0] == target:
            return m
        elif arr[m][0] < target:
            return search_id(m + 1, high, target)
        else:
            return search_id(low, m - 1, target)
    else:
        return -1


class Persons(Resource):
    def get(self):
        curs.execute("SELECT * FROM people ORDER BY id")
        return curs.fetchall()

    def post(self):
        args = post_parser.parse_args()
        curs.execute("INSERT INTO people (name, address, ssn, college) VALUES (%s, %s, %s, %s)", (args["name"], args["address"], args["ssn"], args["college"]))
        conn.commit()
        curs.execute("SELECT max(id) FROM people;")
        person_id = curs.fetchone()[0];
        return Person.get(self, person_id), 201


class Person(Resource):
    def get(self, person_id):
        curs.execute("SELECT * FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            return result

    def put(self, person_id):
        curs.execute("SELECT * FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            args = post_parser.parse_args()
            curs.execute("UPDATE people SET name=%s, address=%s, ssn=%s, college=%s WHERE id="
                         "%s", (args["name"], args["address"], args["ssn"], args["college"], person_id))
            conn.commit()
            return Person.get(self, person_id), 201

    def patch(self, person_id):
        curs.execute("SELECT * FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            args = patch_parser.parse_args()
            if args["name"]:
                curs.execute("UPDATE people SET name=%s WHERE id=%s", (args["name"], person_id))
            if args["address"]:
                curs.execute("UPDATE people SET address=%s WHERE id=%s", (args["address"], person_id))
            if args["ssn"]:
                curs.execute("UPDATE people SET ssn=%s WHERE id=%s", (args["ssn"], person_id))
            if args["college"]:
                curs.execute("UPDATE people SET college=%s WHERE id=%s", (args["college"], person_id))
            conn.commit()
            return Person.get(self, person_id)

    def delete(self, person_id):
        curs.execute("SELECT * FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            curs.execute("DELETE FROM people WHERE id=%s", [person_id])
            conn.commit()
            return "Deleted person with id %s." % person_id


class Name(Resource):
    def get(self, person_id):
        curs.execute("SELECT name FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            return result


class Address(Resource):
    def get(self, person_id):
        curs.execute("SELECT address FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            return result


class Ssn(Resource):
    def get(self, person_id):
        curs.execute("SELECT ssn FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            return result


class College(Resource):
    def get(self, person_id):
        curs.execute("SELECT college FROM people WHERE id=%s", [person_id])
        result = curs.fetchone()
        if not result:
            abort(404, message="Person does not exist.")
        else:
            return result


api.add_resource(Persons, "/api/persons")
api.add_resource(Person, "/api/persons/<int:person_id>")
api.add_resource(Name, "/api/persons/<int:person_id>/name")
api.add_resource(Address, "/api/persons/<int:person_id>/address")
api.add_resource(Ssn, "/api/persons/<int:person_id>/ssn")
api.add_resource(College, "/api/persons/<int:person_id>/college")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
