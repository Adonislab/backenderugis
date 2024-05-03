from django.http import HttpResponse

def index(request):
    message = "Bonjour tout le monde"
    return HttpResponse(message)
