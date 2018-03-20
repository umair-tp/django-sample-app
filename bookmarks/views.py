from django.forms import ModelForm
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Bookmark


class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        exclude = ['owner']

@csrf_exempt
def index(request):
    next = request.POST.get('next', '/bookmarks/')
    if (not request.user.is_authenticated) or (request.user == None):
        return JsonResponse('Unauthorized', status=401, safe=False)
    if Bookmark.objects.filter(url=request.POST.get('url', '/'), owner=request.user).count() != 0:
        return redirect('/bookmarks/')
    bookmark_form = BookmarkForm(request.POST)
    if bookmark_form.is_valid():
        bookmark = bookmark_form.save(commit=False)
        bookmark.owner = request.user
        bookmark.save()
        return HttpResponseRedirect(next)
    else:
        return JsonResponse(bookmark_form.errors, status=402, safe=False)

def list_all(request):
    if (not request.user.is_authenticated) or (request.user == None):
        return redirect('/accounts/login/')
    if request.user.is_superuser:
        return redirect('/admin/')
    bookmark_list = Bookmark.objects.filter(owner = request.user)
    result = ''
    for bookmark in bookmark_list:
        result += "<p><a href='"+bookmark.url+"'>"+bookmark.url+"</a></p>"
    if not bookmark_list:
        result = "You have not added any bookmarks till now!"
    return HttpResponse(result)