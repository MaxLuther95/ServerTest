from django.http import JsonResponse
import datetime

# Create your views here.
def get_uhrzeit(request):
    now = datetime.datetime.now()
    return JsonResponse({"uhrzeit": now.strftime("%H:%M:%S")})