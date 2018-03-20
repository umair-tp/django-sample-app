from django.forms import ModelForm
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ['is_active', 'owner']

@csrf_exempt
def post(request):
    next = request.POST.get('next', '/')
    if (not request.user.is_authenticated) or (request.user == None):
        return JsonResponse('Unauthorized', status=401, safe=False)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.owner = request.user
        comment.save()
        return HttpResponseRedirect(next)
    else:
        return JsonResponse(comment_form.errors, status=402, safe=False)

def fetch_all(request):
    if (not request.user.is_authenticated) or (request.user == None):
        return redirect('/accounts/login/')
    if request.user.is_superuser:
        return redirect('/admin/')
    if (request.POST.get('model','') or request.POST.get('object_id','')):
        return JsonResponse('Check model and object id', status=403, safe=False)
    comment_list = Comment.objects.filter(
        owner = request.user,
        model=request.POST.get('model',''),
        object_id=request.POST.get('object_id','')
    )
    return JsonResponse(list(comment_list), status=200, safe=False)