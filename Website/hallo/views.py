from django.shortcuts import render

# Create your views here.
def hallo(request):
	besucher = request.user.get_username()
	return render(request, "hallo/index.html", {"besucher": besucher})

def hallo2(request):
	return render(request, "hallo/zwei.html")