import json
import os.path
import re
from pathlib import Path

global clients
global clients_id
clients = set()
clients_id = set()


class client:
    def __init__(self, id):
        self.id = id
        clients.add(self)
        clients_id.add(id)

    firstname = str()
    lastname = str()
    phone_number = str()
    graduation_year = str()
    field_of_study = str()
    password = str()
    is_in_group = bool()
    current_menu = "start"


def get_client_by_id(id):
    if (id in clients_id):
        for item in clients:
            if (id == item.id):
                return item
    else:
        return False


def is_user_exist_with_phone_number(phone_number):
    phone_number_str = str(phone_number)
    for filename in os.listdir('../data/'):
        if re.search(phone_number_str, filename):
            with open("../data/" + filename, "r") as file:
                data_dict = json.load(file)
            return True

    return False


def save_client_to_database(client):
    s = make_json_string(client.firstname, client.lastname, client.phone_number, client.graduation_year,
                         client.field_of_study, client.id, client.password)
    save_user(s, client.id, client.phone_number)


def make_json_string(firstname, lastname, phone_number, graduation_year, field_of_study, id, password):
    return json.dumps({"firstname": firstname,
                       'lastname': lastname,
                       'phone_number': phone_number,
                       'graduation_year': graduation_year,
                       'field_of_study': field_of_study,
                       'id': id,
                       'password': password})


def save_user(json_of_user, id, phone_number):
    file = open("../data/" + str(phone_number) + '_' + str(id) + '.json', 'w')
    file.write(json_of_user)
    file.close()


def get_user_json_from_file_phone_number(phone_number):
    for filename in os.listdir('../data/'):
        if re.search(phone_number, filename):
            file = open("../data/" + filename, 'r')
            return json.load(file)


def get_user_json_from_file_id(id):
    id = str('_' + str(id))
    for filename in os.listdir('../data/'):
        if re.search(id, filename):
            file = open("../data/" + filename, 'r')
            return json.load(file)


def is_phone_number_valid(number):
    if (len(number) != 11):
        return False
    if (re.search("09\d{9}", number) == None):
        return False
    if (re.search("09\d{9}", number).start() != 0):
        return False

    return True


def is_graduation_valid(number):
    if (len(number) != 4):
        return False
    if (re.search("1\d{3}", number) == None):
        return False
    if (re.search("1\d{3}", number).start() != 0):
        return False
    return True


def rename_file_for_logout(id):
    id = str('_' + str(id))
    for filename in os.listdir('../data/'):
        if re.search(id, filename):
            old_path = Path("../data/" + filename)
            new_path = Path("../data/" + filename.replace(id, '__________'))
            old_path.rename(new_path)


def rename_file_for_login(phone_number, id):
    id = str('_' + str(id))
    for filename in os.listdir('../data/'):
        if re.search(phone_number, filename):
            old_path = Path("../data/" + filename)
            new_path = Path("../data/" + filename.replace('__________', id))
            old_path.rename(new_path)


def delet_user_with_id(id):
    id = str('_' + str(id))
    for filename in os.listdir('../data/'):
        if re.search(id, filename):
            os.remove('../data/' + filename)
