import json
import os.path
import re

global clients
global clients_id
clients = set()
clients_id = set()

class client:
    def __init__(self , id):
        self.id = id
        clients.add(self)
        clients_id.add(id)
    firstname = str()
    lastname = str()
    phone_number = str()
    graduation_year = str()
    field_of_study = str()
    password = str()
    current_menu = "start"
    


def get_client_by_id(id):
        if(id in clients_id ):
            for item in clients:
                if(id == item.id):
                    return item
        else:
            return False



def save_client_to_database(client):
    s = make_json_string(client.firstname , client.lastname , client.phone_number , client.graduation_year , client.field_of_study , client.id , client.password)
    save_user(s , client.id , client.phone_number)

def make_json_string(firstname , lastname , phone_number , graduation_year  , field_of_study, id , password ):
    return json.dumps({"firstname" :firstname ,
                       'lastname' : lastname ,
                       'phone_number' : phone_number ,
                       'graduation_year': graduation_year ,
                       'field_of_study' : field_of_study ,
                       'id' : id ,
                       'password' : password})


def save_user(json_of_user , id , phone_number):
    file = open("../data/" +str(phone_number)+'_'+ str(id)+ '.json' , 'w')
    file.write(json_of_user)
    file.close()




def is_user_exist_with_phone_number(phone_number):
    if(os.path.exists("../data/" + str(id)+ ".json")):
        return True
    else :
        return False
def get_user_json_from_file(id):
    file = open("../data/" + str(id)+ '.json' , 'r')
    return json.load(file)


def is_phone_number_valid(number):
    if(len(number) != 11):
        return False
    if(re.search("09\d{9}" , number) == None):
        return False
    if(re.search("09\d{9}" , number).start() != 0):
        return False
    return True


def is_graduation_valid(number):
    if(len(number) != 4):
        return False
    if(re.search("1\d{3}" , number) == None):
        return False
    if(re.search("1\d{3}" , number).start() != 0):
        return False
    return True
