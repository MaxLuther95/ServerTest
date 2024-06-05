# In deiner views.py
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import threading

@gzip.gzip_page
def Home(request):
    try:
        return StreamingHttpResponse(gen(cam), content_type = "multipart/x-mixed-replace;boundary=frame")
    except:
        pass

class VideoCamera(object):
    def __init__(self, cam_id):
        self.video = cv2.VideoCapture(cam_id)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target = self.update, args = ()).start()
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

cam = VideoCamera(0)