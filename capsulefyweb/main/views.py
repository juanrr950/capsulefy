from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import ContactForm, NewFreeCapsuleForm, EditFreeCapsuleForm, ModularCapsuleForm, ModuleForm
from .models import Capsule, Module, File
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
from random import randint
import os
from datetime import datetime, timezone
from django.http import HttpResponseNotFound
import smtplib
from django.contrib.auth.views import LoginView


def index(request):
    enterpriseEmail = "capsulefy.communications@gmail.com"
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["Name"]
            email = form.cleaned_data["Email"]
            message = form.cleaned_data["Message"]
            form = ContactForm()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(enterpriseEmail, "aG7nOp4FhG")
            msg = name + "\n" + email + "\n" + message
            msg = msg.encode('utf-8')
            server.sendmail(msg=msg, from_addr=email, to_addrs=[enterpriseEmail])
            return render(request, 'index.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})


def displayCapsules(request, id):
    capsule =  get_object_or_404(Capsule, id=id)
    print(capsule.id)
    creator = False
    if request.user.is_authenticated:
        user = request.user
        if user.id == capsule.creator.id:
            creator = True
    modules = []
    for module in capsule.modules.all():
        if not(creator == False and module.release_date > datetime.now(timezone.utc)):
            modules.append(module)
    modules.sort(key=lambda x: x.pk)
    if len(modules) == 0:
        return HttpResponseNotFound()
    else:
        return render(request, 'capsule/displaycapsule.html', {'capsule': capsule, 'modules': modules})


def createModularCapsule(request):
    user = request.user
    if request.method == 'POST':
        modulesSize = request.POST['modulesSize']
        capsuleForm = ModularCapsuleForm(request.POST)
        if capsuleForm.is_valid():
            capsuleFormulario = capsuleForm.cleaned_data
            title = capsuleFormulario['title']
            emails = capsuleFormulario['emails']
            capsule_type = 'M'
            private = False
            dead_man_switch = False
            dead_man_counter = 0
            twitter = capsuleFormulario['twitter']
            facebook = capsuleFormulario['facebook']
            capsule = Capsule.objects.create(title=title, emails=emails, capsule_type=capsule_type, private=private,
                                             dead_man_switch=dead_man_switch, dead_man_counter=dead_man_counter,
                                             twitter=twitter, facebook=facebook, creator_id=user.id)

            for i in range(int(modulesSize)):
                description = request.POST['description'+str(i)]
                release_date = request.POST['release_date'+str(i)]
                file = request.POST['file'+str(i)]
                # Subir archivo a firebase
                Module.objects.create(description=description, release_date=release_date, capsule_id=capsule.id)

            return HttpResponseRedirect('/')
    else:
        form = ModularCapsuleForm()

    return render(request, 'capsule/modularcapsule.html')


def editModularCapsule(request, pk):
    oldcapsule = get_object_or_404(Capsule, id=pk)
    oldmodule = oldcapsule.modules.first()
    olddata = {
        'title': oldcapsule.title,
        'description': oldmodule.description,
        'release_date': oldmodule.release_date,
        'emails': oldcapsule.emails,
        'twitter': oldcapsule.twitter,
        'facebook': oldcapsule.facebook
    }
    if request.method == 'POST':
        form = ModularCapsuleForm(request.POST)
        if form.is_valid():
            formulario = form.cleaned_data
            oldcapsule.title = formulario['title']
            oldcapsule.emails = formulario['emails']
            oldcapsule.twitter = formulario['twitter']
            oldcapsule.facebook = formulario['facebook']
            oldmodule.description = formulario['description']
            oldmodule.release_date = formulario['release_date']
            oldcapsule.save()
            oldmodule.save()
            return HttpResponseRedirect('/')
    else:
        form = ModularCapsuleForm(initial=olddata)
    return render(request, 'capsule/modularcapsule.html', {'form': form})


class login(LoginView):
    def __init__(self,  *args, **kwargs):
        super(LoginView, self).__init__(*args, **kwargs)


def createFreeCapsule(request):
    if request.method == 'POST':
        form = NewFreeCapsuleForm(request.POST, request.FILES)
        if form.is_valid():
            formulario = form.cleaned_data
            title = formulario['title']
            emails = formulario['emails']
            capsule_type = 'F'
            private = False
            dead_man_switch = False
            dead_man_counter = 0
            twitter = formulario['twitter']
            facebook = formulario['facebook']
            description = formulario['description']
            release_date = formulario['release_date']
            capsule = Capsule.objects.create(title=title, emails=emails, capsule_type=capsule_type, private=private,
                                             dead_man_switch=dead_man_switch, dead_man_counter=dead_man_counter,
                                             twitter=twitter, facebook=facebook, creator_id=2)
            module = Module.objects.create(description=description, release_date=release_date, capsule_id=capsule.id)
            if formulario['file'] is not None:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(settings.FIREBASE_CREDENTIALS)
                client = storage.Client(credentials=credentials, project='capsulefy')
                bucket = client.get_bucket('capsulefy.appspot.com')
                idrand = randint(0, 999)
                filename, fileext = os.path.splitext(formulario['file'].name)
                blob = bucket.blob(title + str(idrand) + fileext)
                blob.upload_from_file(formulario['file'].file, size=formulario['file'].size)
            return HttpResponseRedirect('/')
    else:
        form = NewFreeCapsuleForm()
    return render(request, 'freecapsule.html', {'form': form})


def editFreeCapsule(request, pk):
    oldcapsule = get_object_or_404(Capsule, id=pk)
    oldmodule = oldcapsule.modules.first()
    olddata = {
        'title': oldcapsule.title,
        'description': oldmodule.description,
        'release_date': oldmodule.release_date,
        'emails': oldcapsule.emails,
        'twitter': oldcapsule.twitter,
        'facebook': oldcapsule.facebook
    }
    if request.method == 'POST':
        form = EditFreeCapsuleForm(request.POST)
        if form.is_valid():
            formulario = form.cleaned_data
            oldcapsule.title = formulario['title']
            oldcapsule.emails = formulario['emails']
            oldcapsule.twitter = formulario['twitter']
            oldcapsule.facebook = formulario['facebook']
            oldmodule.description = formulario['description']
            oldmodule.release_date = formulario['release_date']
            oldcapsule.save()
            oldmodule.save()
            return HttpResponseRedirect('/')
    else:
        form = EditFreeCapsuleForm(initial=olddata)
    return render(request, 'freecapsule.html', {'form': form})


def deleteCapsule(request, pk):
    capsule = get_object_or_404(Capsule, id=pk)
    capsule.delete()
    return HttpResponseRedirect('/')

