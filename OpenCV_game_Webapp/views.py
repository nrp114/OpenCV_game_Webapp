from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import cv2
import time
import numpy as np
from . import hand_module as htm
import math

from .hand_module import game

detector = htm.handDetector(detectionCon=0.7)

#camera = cv2.VideoCapture(0)

@gzip.gzip_page
def Home2(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

@gzip.gzip_page
def Home(request):
    try:
        return StreamingHttpResponse(gen2(), content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

def gen2():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        print(success)
        if not success:
            print("False")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


# to capture video class

def score_change(img, score, iswin, target):
    if iswin:
        print("WIN")
    cv2.putText(img, "Score :" + str(score), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
    cv2.putText(img, "Aim :" + str(target), (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        # for (x, y, w, h) in faces_detected:
        # cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()


"""""
class VideoCamera(object):
    time_skip = 100
    time_taken = 0
    final_time = 0

    def __init__(self):
        self.time_taken = time.time()
        self.game = htm.game()
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        img = image
        hand_img = detector.findHands(img)
        hand_pos = detector.findPosition(img, draw=False)
        self.game.drawCircle(img)

        if len(hand_pos) != 0:
            # print(hand_pos)

            x12, y12 = hand_pos[12][1], hand_pos[12][2]
            x16, y16 = hand_pos[16][1], hand_pos[16][2]
            x20, y20 = hand_pos[20][1], hand_pos[20][2]
            x0, y0 = hand_pos[0][1], hand_pos[0][2]
            x1, y1 = hand_pos[4][1], hand_pos[4][2]
            x2, y2 = hand_pos[8][1], hand_pos[8][2]
            x5, y5 = hand_pos[5][1], hand_pos[5][2]
            x4, y4 = hand_pos[4][1], hand_pos[4][2]
            x11, y11 = hand_pos[11][1], hand_pos[11][2]
            x9, y9 = hand_pos[9][1], hand_pos[9][2]

            if self.game.isFinished():
                # print("jkasdn")
                if self.final_time == 0:
                    print("WON")
                    self.final_time = time.time() - self.time_taken
                cv2.putText(img, "WON - time taken:" + str(round(self.final_time, 2)) + "sec", (100, 100),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))
            else:  # print(length_all)
                fist_length = math.hypot(x11 - x4, y11 - y4)

                # print(fist_length)
                score_change(img, self.game.point, self.game.isFinished(), self.game.maxScore)
                if self.game.check_win(fist_length, x9, y9):
                    print("Hit")

        # print(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

"""""

def gen(camera):
    while True:
        frame = None
        try:
            frame = camera.get_frame()
        except:
            print("error")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def index(request):
    return None
