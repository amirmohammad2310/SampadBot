import json
import os.path

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

def get_user_json(id):
    if(os.path.exists("../data/" + str(id)+ ".json")):
        return True
    else :
        return False

