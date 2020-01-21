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

frames = []
counter = 0


list_of_cameras = [
    "http://192.168.1.133"
]

list_of_cam_objects = func.create_list_of_cam_objects(list_of_cameras)

thecam = VideoCamera(list_of_cam_objects[0].fulladress)
thecam2 = VideoCamera(list_of_cam_objects[0].fulladress)
thecam3 = VideoCamera(list_of_cam_objects[0].fulladress)
thecam4 = VideoCamera(list_of_cam_objects[0].fulladress)

def set_current_cam(cam):
    global thecam
    thecam = VideoCamera(list_of_cam_objects[int(cam)-1].fulladress)

def set_current_cam2(cam):
    global thecam2
    thecam2 = VideoCamera(list_of_cam_objects[int(cam)-1].fulladress)

def set_current_cam3(cam):
    global thecam3
    thecam3 = VideoCamera(list_of_cam_objects[int(cam)-1].fulladress)

def set_current_cam4(cam):
    global thecam4
    thecam4 = VideoCamera(list_of_cam_objects[int(cam)-1].fulladress)

def gen(delay):
    global thecam
    global frames
    set_current_cam(0)
    # global counter
    counter = 0
    frames = []
    while True:
        frames.append(thecam.get_frame())
        counter+=1
        if len(frames) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames.pop(0) + b'\r\n\r\n')
        else:
            if len(frames) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames[0] + b'\r\n\r\n')

    thecam.release_cam()

def gen2(delay):
    global thecam2
    global frames2
    set_current_cam2(0)
    # global counter
    counter2 = 0
    frames2 = []
    while True:
        frames2.append(thecam2.get_frame())
        counter2+=1
        if len(frames2) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames2.pop(0) + b'\r\n\r\n')
        else:
            if len(frames2) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames2[0] + b'\r\n\r\n')

    thecam2.release_cam()

def gen3(delay):
    global thecam3
    global frames3
    set_current_cam3(0)
    # global counter
    counter3 = 0
    frames3 = []
    while True:
        frames3.append(thecam3.get_frame())
        counter3+=1
        if len(frames3) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames3.pop(0) + b'\r\n\r\n')
        else:
            if len(frames3) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames3[0] + b'\r\n\r\n')

    thecam3.release_cam()

def gen4(delay):
    global thecam4
    global frames4
    set_current_cam4(0)
    # global counter
    counter4 = 0
    frames4 = []
    while True:
        frames4.append(thecam4.get_frame())
        counter4+=1
        if len(frames4) >= (int(delay)*25):
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames4.pop(0) + b'\r\n\r\n')
        else:
            if len(frames4) > 0:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frames4[0] + b'\r\n\r\n')

    thecam4.release_cam()

app = Flask(__name__)

@app.route("/")
def main():
    """ Main route """
    global frames

    if len(frames) > 0:
        # global thecam
        frames = []
        # del thecam
    return render_template("index.html", data=list_of_cam_objects, cams=list_of_cameras)

@app.route("/selectbox")
def selectbox():
    """ select middle route """
    return render_template("selectbox.html")



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
    # print(request.form)
    delay = int(request.args.get("delay"))
    temp_delay = -1
    if temp_delay != delay:
        temp_delay = delay
    if delay == 0:
        return render_template("one_cam.html", data=list_of_cam_objects[0].fulladress)
    else:
        print("delay: {}".format(temp_delay))
        return render_template("cam.html", delay=temp_delay)

@app.route('/fourcams')
def fourcams():
    # print(request.form)

    return render_template("four_cams.html", delay=2)


@app.route("/selectcam/", defaults={'cam_nr': 0})
@app.route("/selectcam/<int:cam_nr>")
def selectcam(cam_nr):
    """ sel route """
    set_current_cam(cam_nr)
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
