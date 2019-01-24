from classes import api
import cognitive_face as cf

subscription_key = ""
api.init_api(subscription_key)
# 'ilyasovs' is de person group waarin wij heel het project gewerkt hebben, omdat we getest hebben met foto's van Yakub en z'n zus en hun achternaam is Ilyasov(a)

# 'ilyasovs' is de person group, 'Yentl' is de naam van de persoon', 'glasses' is data van de persoon (deze data is niet verplicht)
api.add_person_to_person_group('ilyasovs', 'Yentl', 'glasses')

# dit print alle personen die in de person group 'ilyasovs' zitten, om te tonen dat Yentl er is bij gekomen
for person in cf.person.lists('ilyasovs'):
    print(person["name"])

# 'ilyasovs' is de person group waaruit je de persoon wilt verwijderen, 'Yentl' is de persoon die je wilt verwijderen
api.delete_person_from_person_group('ilyasovs', 'Yentl')

# dit print alle personen die in de person group 'ilyasovs zitten, om te tonen dat Yentl eruit is verwijderd
for person in cf.person.lists('ilyasovs'):
    print(person["name"])

# om een foto toe te voegen aan een bepaalde persoon, deze staat in commentaar, omdat Yentl al verwijderd is en omdat er geen geldige foto wordt meegegeven
# api.add_picture_to_person(image_path, image_name, 'ilyasovs', 'Yentl')

# de person group 'test_group' wordt aangemaakt
# een person group bestaat altijd uit kleine letters en heeft geen spaties in de naam, daarom wordt het person_group_id altijd naar lowercase omgezet en de spaties vervangen door een underscore
# dit gebeurt bij iedere functie in het begin:
#     person_group_id = person_group_id.lower()
#     person_group_id = person_group_id.replace(" ", "_")
api.create_person_group("TeST gROup")

# dit print alle person groups die je hebt op jouw account, om te tonen dat test_group er is bijgekomen
print(cf.person_group.lists())

# verwijdert de person group 'test_group'
api.delete_person_group("TEST groUp")

# dit print alle person groups die je hebt op jouw account, om te tonen dat test_group verwijdert is
print(cf.person_group.lists())