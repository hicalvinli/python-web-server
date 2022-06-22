import requests
import psycopg2

BASE = "http://localhost:8000/api/persons"
conn = psycopg2.connect(host="localhost", port=5432, database="projdb", user="calv", password="postgrescalv622")
curs = conn.cursor()


def test_get_all_people():
    curs.execute("SELECT * FROM people ORDER BY id")
    result = list(curs.fetchall())
    for i in range(len(result)):
        result[i] = list(result[i])
    response = requests.get(BASE).json()
    assert response == result


def test_create_person():
    curs.execute("SELECT id FROM people ORDER BY id DESC")
    response = requests.post(BASE, headers={"Content-type": "application/json"},
                             data="{\"name\": \"Benjamin Franklin\", \"address\": \"444 Fourth Street, Springfield, "
                                  "Illinois\", \"ssn\": 22222222, \"college\": \"University of California "
                                  "Riverside\"}").json()
    assert response == [curs.fetchone()[0] + 1, 'Benjamin Franklin', '444 Fourth Street, Springfield, Illinois',
                        22222222, 'University of California Riverside']


def test_create_without_name():
    response = requests.post(BASE, headers={"Content-type": "application/json"},
                             data="{\"address\": \"444 Fourth Street, Springfield, "
                                  "Illinois\", \"ssn\": 22222222, \"college\": \"University of California "
                                  "Riverside\"}").json()
    assert response == {'message': {'name': 'Name is required.'}}


def test_create_only_name():
    curs.execute("SELECT id FROM people ORDER BY id DESC")
    response = requests.post(BASE, headers={"Content-type": "application/json"},
                             data="{\"name\": \"George Washington\"}").json()
    assert response == [curs.fetchone()[0] + 1, 'George Washington', None, None, None]


def test_get_one_person():
    curs.execute("SELECT * FROM people WHERE id=2")
    response = requests.get(BASE + "/2").json()
    assert response == [2, "Jane Eyre", "222 Second Street, Boston, Massachusetts", 11111111,
                        "Massachusetts Institute of Technology"]


def test_get_invalid_person():
    response = requests.get(BASE + "/999").json()
    assert response == {'message': 'Person does not exist.'}


def test_put():
    response = requests.put(BASE + "/4", headers={"Content-type": "application/json"},
                            data="{\"name\": \"Joe Biden\", \"college\": \"University of Delaware\"}").json()
    assert response == [4, 'Joe Biden', None, None, 'University of Delaware']


def test_put_invalid_person():
    response = requests.put(BASE + "/999", headers={"Content-type": "application/json"},
                            data="{\"name\": \"Joe Biden\", \"college\": \"University of Delaware\"}").json()
    assert response == {'message': 'Person does not exist.'}


def test_patch():
    response = requests.patch(BASE + "/3", headers={"Content-type": "application/json"},
                              data="{\"address\": \"999 Ninth Street, Cambridge, Massachusetts\", \"ssn\": 12345678}").json()
    assert response == [3, "Charles Dickens", "999 Ninth Street, Cambridge, Massachusetts", 12345678,
                        "Harvard University"]


def test_patch_invalid_person():
    response = requests.patch(BASE + "/999", headers={"Content-type": "application/json"},
                              data="{\"address\": \"999 Ninth Street, Cambridge, Massachusetts\", \"ssn\": 12345678}").json()
    assert response == {'message': 'Person does not exist.'}


def test_delete():
    requests.delete(BASE + "/4")
    response = requests.get(BASE + "/4").json()
    assert response == {'message': 'Person does not exist.'}


def test_get_name():
    response = requests.get(BASE + "/1/name").json()
    assert response == ['John Doe']


def test_get_address():
    response = requests.get(BASE + "/2/address").json()
    assert response == ['222 Second Street, Boston, Massachusetts']


def test_get_ssn():
    response = requests.get(BASE + "/3/ssn").json()
    assert response == [12345678]


def test_get_college():
    response = requests.get(BASE + "/1/college").json()
    assert response == ["Stanford University"]
