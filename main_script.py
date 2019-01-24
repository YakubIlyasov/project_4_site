from classes import camera
import time

try:
    class_name = "3NMCT"

    minutes = 0.5
    seconds_wait = 60 * minutes

    cam = camera.init_camera(index_camera=0)

    while True:
        identified_students = camera.capture_image(cam, class_name)
        print("The people in the picture are: ")
        for student in identified_students:
            print("- " + student)
        print("")
        time.sleep(seconds_wait)

except Exception as error:
    print("Error: ", error)

finally:
    print("Programme closing.")
