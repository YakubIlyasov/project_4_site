from flask import Flask
from flask import render_template
from project_4_site.classes import camera
import glob
import os

detected_faces_folder = os.path.join('static', 'images', 'detected_faces')
app = Flask(__name__)
app.config['detected_faces_folder'] = detected_faces_folder


@app.route('/')
def page_startup():
    class_name = "3NMCT"

    cam = camera.init_camera(index_camera=0)
    identified_students = camera.capture_image(cam, class_name)

    txt = "The people in the picture are: "
    for student in identified_students:
        txt += "\n- " + student

    list_of_files = glob.glob('./static/images/detected_faces/*.jpg')  # * means all if need specific format then *.csv
    img = '.' + max(list_of_files, key=os.path.getctime).replace('\\', '/')

    print(txt)
    print(img)

    return render_template("temp_home.html", image_name=img, text=txt)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)