#!/usr/bin/env python3

"""
Ip camera application
"""

# Importera relevanta moduler
from flask import Flask, render_template, make_response, Response, redirect, url_for, request

from videocamera import VideoCamera

import cv2 as cv
from cam import Cam
import functions as func

list_of_cameras = [
"http://192.168.1.133",
"http://192.168.1.133",
"http://192.168.1.133",
"http://192.168.1.133"

]

menu = [
    {
        "choices": [
            "LIVE - Singlecam",
            "LIVE - Doublecam",
            "DELAY - Singlecam",
            "DELAY - Singlecam Quadview",
            "DELAY - Doublecam"
        ],
        "jsmenu": "menu.js"
    },
    {
        "choices": list_of_cameras,
        "delay": False,
        "double": False,
        "jsmenu": "live_single.js"
    },
    {
        "choices": list_of_cameras,
        "delay": False,
        "double": True,
        "jsmenu": "live_double.js"
    },
    {
        "choices": list_of_cameras,
        "delay": True,
        "double": False,
        "jsmenu": "delay_single.js"
    },
    {
        "choices": list_of_cameras,
        "delay": True,
        "quad": True,
        "jsmenu": "delay_single_quad.js"
    },
    {
        "choices": list_of_cameras,
        "delay": True,
        "double": True,
        "jsmenu": "delay_double.js"
    },
]

choices = {
    "choice": "",
    "mode": -1,
    "cams": []
}

frames = []
counter = 0
data = {
    "nr_of_cams": 0,
    "selected_cam": 0,
    "cameras": []
}


list_of_cam_objects = func.create_list_of_cam_objects(list_of_cameras)


def set_cam(cam):
    global data

    data["cameras"].append(VideoCamera(list_of_cam_objects[int(cam)-1].fulladress))

def set_quad_cam(cam):
    global data

    data["cameras"].append(VideoCamera(list_of_cam_objects[int(cam)-1].fulladress))
    data["cameras"].append(VideoCamera(list_of_cam_objects[int(cam)-1].fulladress))
    data["cameras"].append(VideoCamera(list_of_cam_objects[int(cam)-1].fulladress))
    data["cameras"].append(VideoCamera(list_of_cam_objects[int(cam)-1].fulladress))


def gen(delay):
    # global frames
    global data

    counter = 0
    frames = []
    while True:
        frames.append(data["cameras"][0].get_frame())
        counter+=1
        if len(frames) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
        else:
            if len(frames) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames[0] + b'\r\n\r\n')

    data["cameras"][0].release_cam()

def gen2(delay):
    # global thecam2
    # global frames2

    counter2 = 0
    frames2 = []
    while True:
        frames2.append(data["cameras"][1].get_frame())
        counter2+=1
        if len(frames2) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames2.pop(0) + b'\r\n\r\n')
        else:
            if len(frames2) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames2[0] + b'\r\n\r\n')

    data["cameras"][1].release_cam()

def gen3(delay):
    # global thecam3
    # global frames3

    counter3 = 0
    frames3 = []
    while True:
        frames3.append(data["cameras"][2].get_frame())
        counter3+=1
        if len(frames3) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames3.pop(0) + b'\r\n\r\n')
        else:
            if len(frames3) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames3[0] + b'\r\n\r\n')

    data["cameras"][2].release_cam()

def gen4(delay):
    # global thecam4
    # global frames4

    counter4 = 0
    frames4 = []
    while True:
        frames4.append(data["cameras"][3].get_frame())
        counter4+=1
        if len(frames4) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames4.pop(0) + b'\r\n\r\n')
        else:
            if len(frames4) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames4[0] + b'\r\n\r\n')

    data["cameras"][3].release_cam()

app = Flask(__name__)

@app.route("/", defaults={'menu_nr': 0})
@app.route("/<int:menu_nr>")
def main(menu_nr):
    """ Main route """
    # global frames
    global menu
    global choices

    if menu_nr > 0:
        choices["choice"] = menu[0]["choices"][menu_nr-1]

    else:
        choices["choice"] = "Menu"
        data["cameras"] = []

    # if len(frames) > 0:
        # frames = []

    return render_template("index.html", menu=menu[menu_nr], choices=choices)


@app.route("/splashscreen")
def splashscreen():
    """ splashscreen middle route """

    return render_template("splashscreen.html")

@app.route("/selectbox")
def selectbox():
    """ select middle route """

    return render_template("selectbox.html")

@app.route("/setcam/<int:cam>")
def setcam(cam):
    """ setcam middle route """
    global data
    set_cam(cam)
    data["selected_cam"] = cam
    return redirect(url_for("selectbox"))

@app.route("/delta/<int:cam>")
def delta(cam):
    """ delta middle route """
    global data
    set_quad_cam(cam)
    data["selected_cam"] = cam
    return render_template("selectdelta.html")

@app.route('/quad', methods=['GET'])
def quad():
    delay = int(request.args.get("delay"))
    return render_template("four_cams.html", delay=delay)

@app.route('/stream-dual-delay', methods=['GET'])
def stream_dual_delay():
    global data
    delay = int(request.args.get("delay"))
    return render_template("dual_delay.html", delay=delay)


@app.route("/choosecam/", defaults={'cam_nr': 0})
@app.route("/choosecam/<int:cam_nr>")
def choosecam(cam_nr):
    """ choose cam middle route """
    global data
    print("Cam number: {}".format(cam_nr))

    if cam_nr > 0:
        data["selected_cam"] = cam_nr
        data["camera_object"] = VideoCamera(list_of_cam_objects[cam_nr-1].fulladress)
        return render_template("index.html", data=list_of_cam_objects, menu=3)

    return render_template("index.html", data=list_of_cam_objects, menu=2)



@app.route("/select-dual-cams/<int:left>/<int:right>")
def select_dual_cam(left, right):
    """ select_dual_cam route """
    left = list_of_cam_objects[left-1].fulladress
    right = list_of_cam_objects[right-1].fulladress

    return render_template("dual.html", left=left, right=right)

@app.route("/select-dual-cams-delay/<int:left>/<int:right>")
def select_dual_cam_delay(left, right):
    """ select_dual_cam_delay route """
    set_cam(left)
    set_cam(right)
    left = list_of_cam_objects[left-1].fulladress
    right = list_of_cam_objects[right-1].fulladress

    return render_template("selectdualdelay.html", left=left, right=right)

@app.route('/delaystream/<int:delay>')
def delaystream(delay):
    return Response(gen(delay), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/delaystream2/<int:delay>')
def delaystream2(delay):
    return Response(gen2(delay), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/delaystream3/<int:delay>')
def delaystream3(delay):
    return Response(gen3(delay), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/delaystream4/<int:delay>')
def delaystream4(delay):
    return Response(gen4(delay), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stream', methods=['GET'])
def stream():
    global data

    delay = int(request.args.get("delay"))
    temp_delay = -1
    if temp_delay != delay:
        temp_delay = delay
    if delay == 0:
        return render_template("one_cam.html", data=list_of_cam_objects[data["selected_cam"]-1].fulladress)
    else:
        print("delay: {}".format(temp_delay))
        return render_template("cam.html", delay=temp_delay)

@app.route('/fourcams')
def fourcams():

    return render_template("four_cams.html", delay=2)


@app.route("/selectcam/", defaults={'cam_nr': 0})
@app.route("/selectcam/<int:cam_nr>")
def selectcam(cam_nr):
    """ sel route """
    set_cam(cam_nr)
    print("Cam number: {}".format(cam_nr))

    return redirect(url_for("stream", delay=0))


@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument
    import traceback
    return "<p>Flask 500<pre>" + traceback.format_exc()

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
