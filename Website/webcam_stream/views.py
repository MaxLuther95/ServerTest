# In deiner views.py
import cv2
from django.http import StreamingHttpResponse

def capture_video_from_cam():
    # Initialisiere den VideoCapture nur einmal, um Konflikte zu vermeiden
    caps = []
    caps.append(cv2.VideoCapture(filename="/dev/video0"))
    #caps.append(cv2.VideoCapture(filename="/dev/video1")) #nicht möglich
    #caps.append(cv2.VideoCapture(filename="/dev/media3")) #nicht möglich

    while True:
        for cap in caps:
            _, frame = cap.read()
            frame = cv2.flip(frame, 1) # Spiegelt das aktuelle Frame horizontal
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

def show_video_on_page(request):
    return StreamingHttpResponse(capture_video_from_cam(), content_type="multipart/x-mixed-replace;boundary=frame")