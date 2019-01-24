import os
import cv2
import time

from skimage.io import imread
import cognitive_face as cf


def init_api():
    sub_key = '8a79070b7dfe49eab8705eed47cdc581'
    base_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/'
    cf.BaseUrl.set(base_url)
    cf.Key.set(sub_key)
    print("Init api finished!")


def detect_people(image_path, image_name, class_name):
    response = cf.face.detect(image_path + image_name)
    lst_faces = []
    lst_face_id = []
    image_boxes = ""

    image = imread(os.path.join(image_path + image_name))
    image_for_faces = imread(os.path.join(image_path + image_name))

    for index in range(0, len(response)):
        x1 = response[index]["faceRectangle"]["left"]
        x2 = response[index]["faceRectangle"]["left"] + response[index]["faceRectangle"]["width"]
        y1 = response[index]["faceRectangle"]["top"]
        y2 = response[index]["faceRectangle"]["top"] + response[index]["faceRectangle"]["height"]
        print("Coördinates person %s calculated." % index)
        print("")

        image_boxes = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        lst_faces.append(image_for_faces[y1:y2, x1:x2])
        lst_face_id.append(response[index]["faceId"])

    img_name = "%s_%s_%s.jpg" % (class_name, time.strftime("%d_%m_%Y"), time.strftime("%H_%M_%S"))

    path = './static/images/detected_faces/'

    if not os.path.exists(path):
        os.makedirs(path)

    if lst_face_id != []:
        cv2.imwrite(os.path.join(path, img_name), cv2.cvtColor(image_boxes, cv2.COLOR_RGB2BGR))
        return lst_face_id

    else:
        return "No faces detected."


def identify_people(detected_people):
    if detected_people == "No faces detected.":
        return "No faces detected."
    else:
        lst_identified_people = []
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
        return lst_identified_people


def get_person_group_id_for_identify():
    return cf.person_group.lists()[1]["personGroupId"]


def get_people():
    dict_students = {}

    var_person_group = get_person_group_id_for_identify()

    for person in cf.person.lists(var_person_group):
        dict_students[str(person["personId"])] = person["name"]
    return dict_students
