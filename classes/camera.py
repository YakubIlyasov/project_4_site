import os
import cv2
import time

from project_4_site.classes import api

init_counter = 0


def init_camera(index_camera=0, frm_width=1920, frm_height=1080):
    api.init_api()
    cam = cv2.VideoCapture(index_camera)  # 0 -> index of camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, frm_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frm_height)
    print("Init camera finished!")
    return cam


def capture_image(cam, class_name):
    image_captured, img = cam.read()
    print("Image captured: ", image_captured)

    global init_counter

    if image_captured:  # frame captured without any errors
        image_path = "./static/images/" + class_name + "/"

        if not os.path.exists(image_path):
            os.makedirs(image_path)

        img_name = "%s_%s_%s.jpg" % (class_name, time.strftime("%d_%m_%Y"), time.strftime("%H_%M_%S"))

        cv2.imwrite(image_path + img_name, img)  # save image
        print("Image name: ", img_name)

        return api.identify_people(api.detect_people(image_path, img_name, class_name))