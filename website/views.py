from PIL import Image as IMG
import os

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt

from website.models import Gallery, Image
from website.forms import UploadForm

def index(request):
    tpl = "polaroid/index.html"
    ctxt = dict()
    if request.user.is_authenticated:
        ctxt["galleries"] = Gallery.objects.all().filter(owner=request.user)
        ctxt["cover"] = list()
    return render(request, tpl, ctxt)

@login_required
def create_gallery(request):
    g = Gallery(owner=request.user)
    g.save()
    return redirect("gallery", g.id)

def cover_gallery(request, gid):
    gal = get_object_or_404(Gallery, id=gid)
    cover = gal.cover
    if cover is None:
        cover = gal.image_set.first()
    if cover is None:
        return HttpResponse(gid + ";" + "placeholder" + ";svg")
    else:
        return HttpResponse(gid + ";" + cover.id + ";" +
                os.path.splitext(str(cover.path))[1])

def name_gallery(request, gid):
    gal = get_object_or_404(Gallery, id=gid)
    name = gal.name
    if name is None:
        return HttpResponse("")
    else:
        return HttpResponse(gid + ";" + name)

@login_required
@csrf_exempt
def set_name_gallery(request, gid):
    try:
        name = request.POST["name"]
    except KeyError:
        return HttpResponse("KO")
    gal = get_object_or_404(Gallery, id=gid)
    if gal is None or gal.owner != request.user:
        return HttpResponse("KO")
    if name == "":
        return HttpResponse("KO")
    gal.name = name
    gal.save()
    return HttpResponse("OK")

@login_required
def set_cover_gallery(request, gid, mid):
    gal = get_object_or_404(Gallery, id=gid)
    if gal is None or gal.owner != request.user:
        return HttpResponse("KO")
    img = gal.image_set.get(id=mid)
    if img is None or img.owner != request.user:
        return HttpResponse("KO")
    gal.cover = img
    gal.save()
    return HttpResponse("OK")

def gallery(request, gid):
    tpl = "polaroid/gallery.html"
    ctxt = dict()
    gal = get_object_or_404(Gallery, id=gid)
    ctxt["gal"] = gal 
    imgs = []
    for img in gal.image_set.all():
        imgs.append({"id": img.id, "ext": os.path.splitext(str(img.path))[1]})
    ctxt["imgs"] = imgs
    ctxt["form"] = UploadForm(initial={"gallery": gid})
    return render(request, tpl, ctxt)

@login_required
def remove_img(request, mid):
    img = get_object_or_404(Image, id=mid)
    if img.owner != request.user:
        return HttpResponse("KO")
    img.delete()
    return HttpResponse("OK")

@login_required
def remove_gallery(request, gid):
    gal = get_object_or_404(Gallery, id=gid)
    if gal.owner != request.user:
        return HttpResponse("KO")
    for img in gal.image_set.all():
        img.delete()
    gal.delete()
    return HttpResponse("OK")

@login_required
def upload(request):
    if request.method != "POST":
        # Handle this properly (error message)
        return redirect("index")
    form = UploadForm(request.POST, request.FILES)
    try:
        if form.is_valid(request.user):
            form.save(request.FILES["path"], request.user)
            return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(status=415)
    return HttpResponse("KO")


## User management ##

def register(request):
    """
        Registration of new users
        redirect to index if registration succeed
    """
    ctxt = dict()
    tpl = "registration/register.html"
    # Get registration form from POST values
    reg_form = UserCreationForm(request.POST or None, label_suffix='')
    # Check the form validity
    if reg_form.is_valid():
        # Register the new user
        new_user = reg_form.save()
        # Authenticate
        new_user = authenticate(username=new_user.username, password=request.POST["password1"])
        # Log the new user in
        login(request, new_user)
        return redirect("index")
    else:
        # Else we show a registration form
        ctxt["reg_form"] = reg_form
        return render(request, tpl, ctxt)


def crop(request, mid):
    img = get_object_or_404(Image, id=mid)
    if img.owner != request.user:
        return HttpResponse("KO")
    img.crop(16.0/9.0)
    img.save()
    return HttpResponse("OK;" + str(img.id))
