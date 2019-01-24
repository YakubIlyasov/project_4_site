from classes import api
import cognitive_face as cf

subscription_key = ""
api.init_api(subscription_key)

api.add_person_to_person_group('ilyasovs', 'Yentl', 'glasses')

for person in cf.person.lists('ilyasovs'):
    print(person["name"])


api.delete_person_from_person_group('ilyasovs', 'Yentl')

for person in cf.person.lists('ilyasovs'):
    print(person["name"])


# api.add_picture_to_person()

api.create_person_group("TeST gROup")
print(cf.person_group.lists())

api.delete_person_group("TEST groUp")
print(cf.person_group.lists())