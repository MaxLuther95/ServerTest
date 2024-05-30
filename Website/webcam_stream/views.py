from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import threading

class VideoCamera:
    def __init__(self):
        # Initialisierung der Webcam
        self.video = cv2.VideoCapture(0)
        # Erfassen des ersten Frames
        (self.grabbed, self.frame) = self.video.read()
        # Starten eines Threads, um den Frame kontinuierlich zu aktualisieren
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        # Freigabe der Webcam-Ressourcen beim Beenden
        self.video.release()

    def get_frame(self):
        # Erfassen des aktuellen Frames und Kodieren als JPEG
        _, jpeg = cv2.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def update(self):
        while True:
            # Aktualisierung des Frames
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        # Generieren des Streams für die Live-Übertragung
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Erstelle eine globale Instanz der VideoCamera-Klasse
global_cam = VideoCamera()

# Dekorator, der die Antwort komprimiert, bevor sie an den Client gesendet wird
@gzip.gzip_page
def livefe(request):
    try:
        # Verwende die globale Instanz der VideoCamera-Klasse
        return StreamingHttpResponse(gen(global_cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
