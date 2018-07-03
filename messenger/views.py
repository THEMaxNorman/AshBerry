from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from models import  Massage,App, Wish, memeDef
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from messenger.forms import SignUpForm, message, newApp, makeAWish, memeDefForm
import datetime
import pytz
import time
from background_task import background
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from collections import OrderedDict
import random
utc=pytz.UTC
times = [4,8,12,16,20,24]

from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
def get_all_apps(user):
    apps = user.profile.installed_apps
    ends = apps.split(',')
    end = []
    for x in ends:
        end.append(x.split(';'))
    return end

def get_all_unread(user):
    endC = 0
    for x in User.objects.all():
        endC += get_unread_msg_by_user(x,user)
    return endC
# Create your views here.
@login_required
def home(request):
    end = get_all_apps(request.user)
    print end
    uM = get_all_unread(request.user)
    for x in User.objects.all():
        #resetter SHOULD BE COMMENTED BEFORE PRODUCTION
        #x.profile.installed_apps = 'gmail;https://gmail.com,calculator;/calc,contacts;/contacts,appstore;/appstore,settings;/settings,makeAWish;/makeawish'
        x.profile.save()
    return render(request, 'home.html', {'apps': end, 'uM': uM})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form , })
# DO NOT SORT BY TIME!!! IT IS NOT WORTH IT. INSTEAD SORT BY ID!!!
@login_required
def messagesMain(request):
    end = []
    enD = []
    final_list = []
    for x in Massage.objects.all():
        if x.receiver == request.user:
            end.append(x.sender)

    ends = (OrderedDict.fromkeys(end))
    for x in ends:
        if x:
            enD.append(x)

    for usr in enD:
        final_list.append([usr, get_unread_msg_by_user(usr, request.user)])

    return render(request, 'mainMessage.html', {'names': final_list , })

def get_unread_msg_by_user(usr, owner):
    count = 0
    for x in Massage.objects.all():
        if x.sender == owner:
            if x.receiver == usr:
                if x.read == True:
                    count += 1
    return count


# DO NOT SORT BY TIME!!! IT IS NOT WORTH IT. INSTEAD SORT BY ID!!!
@login_required
def messageFrom(request, string):
    other = User.objects.get(id= int(string))
    sent_by_user = []
    reced_by_user = []
    if request.method == 'POST':
        form = message(request.POST)
        msg = form.save()
        msg.sender = request.user
        msg.receiver = other
        msg.save()
        return redirect('/messages/'+string)
    else:
        for x in Massage.objects.all():
            if x.sender == request.user:
                if x.receiver == other:
                    reced_by_user.append(x.id)
            if x.receiver == request.user:
                if x.sender == other:
                    sent_by_user.append(x.id)
        a = sent_by_user + reced_by_user
        a.sort()
        readMessages(getMessageByID(reced_by_user))
        usrSent = getMessageByID(a)
        form = message
        return render(request, 'message.html', {'usrSent': usrSent,'form': form ,'other':other })
#gets each message by its id
#this is done to make sorting simple- instead of sorting by time which is annoying, sort by id which is in order!
def getMessageByID(ls):
    end = []
    for x in ls:
        end.append(Massage.objects.get(id = x))
    return end
#sets all messages in a list to be read
def readMessages(ls):
    for msg in ls:
        msg.read = True
        msg.save()
@login_required
def newMessage(request, string):
    other = User.objects.get(id=int(string))
    if request.method == 'POST':
        form = message(request.POST)
        msg = form.save()
        msg.sender = request.user
        msg.receiver = other
        msg.save()
        return redirect('/messages/'+string)

    else:
        form = message
        return render(request, 'newMessage.html', {'form': form ,'other':other })
@login_required
def contacts(request):
    end = []
    for x in User.objects.all():
        end.append(x)

    return render(request, 'contacts.html', {'end':end})

@login_required
def calc(request):
    return render(request, 'calc.html')

#adds the app to the users apps
def add_app(user, app):
    if check_app(user,app):
        a = user.profile.installed_apps
        user.profile.installed_apps= a + app
        user.profile.save()
def check_app(user,app):
    apps = get_all_apps(user)
    z = app.split(';')
    for x in apps:
        if x[1] == z[1]:
            return False
    return True
@login_required
def appStore(request):
    end = []
    for x in App.objects.all():
        if x.active == True:
            end.append(x)
    return render(request,'appStore.html', {'names':end})

@login_required
def app(request, string):
    theApp = App.objects.get(id=int(string))
    if request.method == 'POST':
        if request.POST.get("id"):
            theApp.active = not theApp.active
            theApp.save()
        else:
            x = (','+ theApp.name+ ';'+ theApp.link)
            add_app(request.user, x )
        return redirect('/')
    else:
        if request.user == theApp.poster:
            return render(request, 'app.html', {'app': theApp, 'bool': True})
        else:
            return render(request, 'app.html', {'app': theApp, 'bool': False})

@login_required
def createNewApp(request):
    if request.method == 'POST':
        form = newApp(request.POST)
        app = form.save()
        app.poster = request.user
        app.save()
        return redirect('/app/'+str(app.id))
    else:
        form = newApp
        return render(request, 'signup.html', {'form': form, })
    print ('done')

@login_required
def yapps(request):
    end = []
    for x in App.objects.all():
        if x.poster == request.user:
            end.append(x)
    return render(request, 'yapps.html', {'names': end} )

@login_required
def play_pop(request):
    return render(request,'pop.html')

def rejoinApp(listOfApps):
    end = ''
    mid = []
    for x in listOfApps:
        mid.append(x[0]+';'+ x[1] + ',')
    for y in mid:
        end += y
    end = end [:-1]
    return end


def remove_app(user, app):

    list_of_apps = get_all_apps(user)
    print list_of_apps
    for x in list_of_apps:
        if x[0] == app.name:
            print ('removing ' + x[0])
            list_of_apps.remove(x)
    print list_of_apps
    user.profile.installed_apps = rejoinApp(list_of_apps)
    user.profile.save()


@login_required
def settings(request):
    if request.method == 'POST':
        appName = request.POST.get("id")
        print appName
        for x in App.objects.all():
            print x.name + ' / ' + appName
            if x.name == str(appName):
                print 'began Removal'
                remove_app(request.user,x)
        return redirect('/')

    else:
        end = get_all_apps(request.user)
        return render(request, 'settings.html', {'end':end})

@login_required
def make_a_wish(request):
    if request.method == 'POST':
        time = str(request.POST.get("id"))
        if time == '11:11':
            form = makeAWish(request.POST)
            wish = form.save()
            wish.save()
        return redirect('/')
    else:
        form = makeAWish
        return render(request, 'makeAWish.html', {'form': form})
@login_required
def shankvstrump(request):
    if request.method == 'POST':
        #save high score
        print('saving score')

    else:
        return render(request, 'shankvstrump.html')

@login_required
def  fishingForWish(request):
    endVar = random.choice(makeAWish.objects.all())
    return render(request, 'fishing.html',{'wish':endVar})

@login_required
def memeUpload(request):
    if request.method == 'POST':
        form = memeDefForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form.poster = request.user
            form.save()
            return redirect('/memeDict')
    else:
        form = memeDefForm()
    return render(request, 'memeDefUpload.html', {'form': form})

@login_required
def memeDict(request):
    end = []
    for x in memeDef.objects.all():
        #preform logic of some sort
        end.append(x)

    return render(request, 'memeDict.html',{'end':end})
@login_required
def meme(request, string):
    mem = memeDef.objects.get(id=int(string))
    return render(request, 'meme.html', {'meme':mem})
@login_required
def ymeme(request):
    print ('fuck')