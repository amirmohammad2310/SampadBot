import json
import os.path

global clients
global clients_id
clients = set()
clients_id = set()

class client:
    def __init__(self , id):
        self.id = id
        clients.add(self)
        clients_id.add(id)
    firstname = None
    current_menu = "start"
    


def get_client_by_id(id):
        if(id in clients_id ):
            for item in clients:
                if(id == item.id):
                    return item
        else:
            return False





def make_json_string(firstname , lastname , phone_number , graduation_year  , field_of_study, id , password ):
    return json.dumps({"firstname" :firstname ,
                       'lastname' : lastname ,
                       'phone_number' : phone_number ,
                       'graduation_year': graduation_year ,
                       'field_of_study' : field_of_study ,
                       'id' : id ,
                       'password' : password})


def save_user(json_of_user , id):
    file = open("../data/" + str(id)+ '.json' , 'w')
    file.write(json_of_user)
    file.close()

def is_user_json(id):
    if(os.path.exists("../data/" + str(id)+ ".json")):
        return True
    else :
        return False
def get_user_json(id):
    file = open("../data/" + str(id)+ '.json' , 'r')
    return json.load(file)
