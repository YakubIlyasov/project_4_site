import os
import cv2
import time

from skimage.io import imread
import cognitive_face as cf


def init_api(subscription_key):
    sub_key = subscription_key
    base_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'
    cf.BaseUrl.set(base_url)
    cf.Key.set(sub_key)
    print("Init api finished!")


def detect_people(image_path, image_name, class_name):
    response = cf.face.detect(image_path + image_name)
    lst_faces = []
    lst_face_id = []
    image_boxes = ""

    # image wordt ingelezen
    image = imread(os.path.join(image_path + image_name))
    # 2e zelfde image wordt ingelezen, om de kaders op te tekenen
    image_for_faces = imread(os.path.join(image_path + image_name))

    for index in range(0, len(response)):
        # coördinaten uit de json halen
        x1 = response[index]["faceRectangle"]["left"]
        x2 = response[index]["faceRectangle"]["left"] + response[index]["faceRectangle"]["width"]
        y1 = response[index]["faceRectangle"]["top"]
        y2 = response[index]["faceRectangle"]["top"] + response[index]["faceRectangle"]["height"]
        print("Coördinates person %s calculated." % index)
        print("")

        # kaders rond de gezichten tekenen
        image_boxes = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        lst_faces.append(image_for_faces[y1:y2, x1:x2])
        lst_face_id.append(response[index]["faceId"])

    # naam voor de nieuwe afbeelding aanmaken
    img_name = "%s_%s_%s.jpg" % (class_name, time.strftime("%d_%m_%Y"), time.strftime("%H_%M_%S"))

    # het pad waar de afbeeldingen met de kaders worden opgeslagen
    path = './static/images/' + class_name + '_detected_faces/'

    # als de map nog niet bestaat, wordt deze aangemaakt
    if not os.path.exists(path):
        os.makedirs(path)

    # de nieuwe afbeelding, met de kaders, wordt opgeslagen als er gezichten gedetecteerd werden
    if lst_face_id != []:
        cv2.imwrite(os.path.join(path, img_name), cv2.cvtColor(image_boxes, cv2.COLOR_RGB2BGR))
        return lst_face_id

    else:
        return "No faces detected."


def identify_people(detected_people):
    # als er geen gezichten gevonden zijn, wordt de identify functie ook niet uitgevoerd
    if detected_people == "No faces detected.":
        return "No faces detected."
    else:
        # lijst waarin alle geïdentificeerde personen opgeslagen zullen worden
        lst_identified_people = []
        # de identify api call wordt uitgevoerd op de gedetecteerde gezichten
        identified_faces = cf.face.identify(detected_people, get_person_group_id_for_identify())
        detected_face = 0

        dict_people = get_people()

        for face in identified_faces:
            if face["candidates"] != []:
                print("We are %.2f%% sure that person %s is %s." % (
                    face["candidates"][0]["confidence"] * 100, detected_face,
                    dict_people[face["candidates"][0]["personId"]]))

                person = "%s | person: %s | percent: %.2f%%" % (
                    dict_people[face["candidates"][0]["personId"]], detected_face,
                    face["candidates"][0]["confidence"] * 100)
                # lst_identified_people.append(dict_people[face["candidates"][0]["personId"]])
                lst_identified_people.append(person)
            else:
                print("We were unable to identify person " + str(detected_face) + ".")
            detected_face += 1
        # de lijst van de geïdentificeerde personen wordt gereturned, om te kunnen weten wie er in de foto staat
        return lst_identified_people


def get_person_group_id_for_identify():
    # om het person group id van de person group te krijgen
    # dit staat op een standaard waarde
    # bij ons is dit de 1e person group, omdat we deze hebben gebruikt om te testen
    # als je meerdere person groups hebt zal je de 0 in de index moeten veranderen
    return cf.person_group.lists()[0]["personGroupId"]


def get_people():
    # deze functie geeft een dictionary terug met daarin alle personId's in de person_group met de daaraangekoppelde naam van de persoon
    # dit wordt gebruikt om de teruggekregen personId om te zetten in de naam van de persoon
    dict_students = {}

    var_person_group = get_person_group_id_for_identify()

    for person in cf.person.lists(var_person_group):
        dict_students[str(person["personId"])] = person["name"]
    return dict_students



def add_picture_to_person(image_path, image_name, person_group_id, person_name):
    # functie om een foto toe te voegen aan een bepaalde persoon in een person group
    person_group_list = []
    dict_people = {}
    list_people = []

    try:
        # checken of de image kan ingelezen te worden om zeker te zijn dat de image bestaat
        img = imread(os.path.join(image_path, image_name))

        for person_group in cf.person_group.lists():
            # lijst van alle person group id's
            person_group_list.append(person_group["personGroupId"])

        if person_group_id in person_group_list:
            # de meegegeven person group moet bestaan
            print("Person group id exists.")

            for person in cf.person.lists(person_group_id):
                # dictionary met de naam van de personen met daaraan hun personId gekoppeld
                dict_people[person["name"]] = person["personId"]
                # lijst met de namen van alle personen
                list_people.append(person["name"])

            if person_name in list_people:
                # je geeft de naam mee in het begin en deze wordt hier omgezet naar het juiste personId
                person_id = dict_people[person_name]

                # als zowel de image, de person group en de persoon zelf bestaan, dan wordt de afbeelding toegevoegd aan deze persoon in de person group
                cf.person.add_face(image_path + image_name, person_group_id, person_id)

            else:
                print("This person does not exist in this person group.")
        else:
            print("Person group id does not exists.")
    except FileNotFoundError as error:
        # als de afbeelding niet gevonden kan worden
        print(error)


def add_person_to_person_group(person_group_id, name, user_data=""):
    # functie om een persoon toe te voegen aan een bepaalde person_group
    # user data is optioneel, dit hoeft niet meegegeven worden
    person_group_list = []
    dict_people = {}
    list_people = []

    for person_group in cf.person_group.lists():
        # lijst met alle person group id's
        person_group_list.append(person_group["personGroupId"])

    if person_group_id in person_group_list:
        # de person group moet bestaan om er een persoon aan te kunnen toevoegen
        print("This person group exists.")

        for person in cf.person.lists(person_group_id):
            # een lijst met alle personen in de person group
            list_people.append(person["name"])

        if name in list_people:
            # als de persoon al bestaat in de person group
            print("This person already exists in this person_group.")
        else:
            # als de persoon nog niet bestaat, wordt deze aangemaakt
            cf.person.create(person_group_id, name, user_data)
    else:
        # als de person group niet bestaat
        print("This person group doesn't exist.")


def create_person_group(person_group_name):
    # functie om een person group aan te maken
    person_group_list = []

    for person_group in cf.person_group.lists():
        # een lijst met alle bestaande person groups
        person_group_list.append(person_group["personGroupId"])

    if person_group_id in person_group_list:
        # de person group mag nog niet bestaan
        print("This person group already exists.")
    else:
        # als de person group nog niet bestaat, wordt deze aangemaakt
        cf.person_group.create(person_group_id)


def delete_person_group(person_group_id):
    # functie om een bestaande person group te verwijderen
    person_group_list = []

    for person_group in cf.person_group.lists():
        # een lijst met alle bestaande person groups
        person_group_list.append(person_group["personGroupId"])

    if person_group_id in person_group_list:
        # de person group moet bestaan om deze te kunnen verwijderen
        print("This person group exists.")
        # de person group wordt verwijderd
        cf.person_group.delete(person_group_id)
        print("Person group " + person_group_id + " got deleted.")
    else:
        # als de person group niet bestaat
        print("This person group does not exist.")