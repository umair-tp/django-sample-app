import requests, logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.forms import ModelForm
from django.http import HttpResponse, JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from comments.models import Comment
from .serializers import PhotoSerializer
from .models import Photo


class PhotoCreateReadView(ListCreateAPIView):
    model = Photo
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    model = Photo
    queryset = Photo.objects.all()[0]
    serializer_class = PhotoSerializer

class PhotoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(PhotoForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
    class Meta:
        model = Photo
        fields = ['photo', ]


@api_view(['GET'])
@csrf_exempt
def photos_list(request) :

    permission_classes = (permissions.IsAuthenticated,)

    if not request.user.is_authenticated:
        return JsonResponse('Unauthorized1', status=401, safe=False)

    if request.method == 'GET':
        photos = Photo.objects.filter(owner=request.user)
        serializer = PhotoSerializer(photos, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def index(request):
    photoForm = PhotoForm()
    alert_script = False
    if (not request.user.is_authenticated) or (request.user == None):
        return redirect('http://localhost:8000/accounts/login/')
    if request.user.is_superuser:
        return redirect('http://localhost:8000/admin/')
    if request.method == "POST":
        #formData = request.POST.copy()
        #formData['owner'] = request.user.id
        photoForm = PhotoForm(request.POST, request.FILES)
        if photoForm.is_valid():
            #photoForm.save()
            photo = photoForm.save(commit=False)
            photo.owner = request.user
            photo.save()
            alert_script = True
    #photoForm = "<form method='post' action='' enctype='multipart/form-data' style='padding: 20px; border: 5px solid grey; float: left;'>" + "<h3>Add more photos:</h3>" + photoForm.as_table() +\
                #"<input type='submit' value='Submit' /></form>"

    #result += "<h2>Hi, "+request.user.username+"!</h2>"
    #result += "<a href='http://localhost:8000/accounts/logout/' style='float: right;'><button class='button' style='vertical-align:middle' type='submit'><span>Logout</span></button></a>"
    #result += "<a href='http://localhost:8000/accounts/password_change/' style='float: right;'><button class='button' style='vertical-align:middle; width: 250px; background: grey;' type='submit'><span>Change Password</span></button></a></br></br>"
    #result += photoForm
    #result += "<div style='margin-top: 150px;'>"
    #for photo in Photo.objects.filter(owner=request.user):
        #result += "<center><a href='"+photo.photo.url+"'><img src='"+photo.photo.url+"' alt='Photo' style='width: 50%; margin: 20px; border: solid grey 5px; padding: 20px;'/></a></center>"
    #if Photo.objects.filter(owner=request.user).count() == 0:
        #result += "<h2>Add photo to see your photos here!</h2>"
    #result += "</div>"

    photo_list = Photo.objects.filter(owner=request.user).order_by("-id")
    template = loader.get_template('photo/index.html')
    api_response = ""#requests.get('http://localhost:8000/photo/api/photos/')
    logging.info(msg=str(api_response))

    context = {
        'photo_list': photo_list,
        'photoForm': photoForm,
        'user': request.user,
        'alert_script': alert_script,
        'response': str(""),#api_response.content),
        'comment_list': Comment.objects.filter(
            model='p'
        ),
    }

    return HttpResponse(template.render(context, request))