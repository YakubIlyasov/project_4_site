from flask import Flask
from flask import render_template
from classes import camera
import glob
import os
from skimage.io import imread

detected_faces_folder = os.path.join('static', 'images', 'detected_faces')
app = Flask(__name__)
app.config['detected_faces_folder'] = detected_faces_folder


@app.route('/')
def page_startup():
    class_name = ""
    subscription_key = ""

    try:
        cam = camera.init_camera(subscription_key, index_camera=1)

        identified_students = camera.capture_image(cam, class_name)
        print(identified_students)

        if identified_students == "No faces detected.":
            txt = "There were no faces detected in the picture."
            list_of_files = glob.glob('./static/images/' + class_name + '/*.jpg')
            img = '.' + max(list_of_files, key=os.path.getctime).replace('\\', '/')
            print(txt)
        else:
            if identified_students != []:
                txt = "The people in the picture are: "
                for student in identified_students:
                    txt += "\n- " + student
            else:
                txt = "The people in the picture were not recognized."

            list_of_files = glob.glob('./static/images/' + class_name + '_detected_faces/*.jpg')  # * means all if need specific format then *.csv
            img = '.' + max(list_of_files, key=os.path.getctime).replace('\\', '/')

            print(txt)
            print(img)

        return render_template("temp_home.html", image_name=img, text=txt)

    except Exception as error:
        print(error)
        img = "../static/site_images/error.jpg"
        img = img.replace("\\", "/")
        return render_template("temp_home.html", image_name=img, text=error)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
