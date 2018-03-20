
from django.template import loader
from django.http import HttpResponse

def index(request):
    context = {}
    template = loader.get_template('homepage.html')
    return HttpResponse(template.render(context, request))