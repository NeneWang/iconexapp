#CORE
from os.path import join
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

#authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages, auth


import time

#firebase
import pyrebase

from django.http import HttpResponse

#ICON
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.wallet.wallet import KeyWallet

from iconsdk.signed_transaction import SignedTransaction
from iconsdk.builder.transaction_builder import (
    TransactionBuilder,
    DeployTransactionBuilder,
    CallTransactionBuilder,
    MessageTransactionBuilder
)

import uuid 

### FIREBASE
config = {
    'apiKey': "AIzaSyCdQLwyRY4nLgG2H0Wo_XgMT2E-LFWGu7k",
    'authDomain': "hack-apps-845b7.firebaseapp.com",
    'databaseURL': "https://hack-apps-845b7.firebaseio.com",
    'projectId': "hack-apps-845b7",
    'storageBucket': "hack-apps-845b7.appspot.com",
    'messagingSenderId': "200715322436",
    'appId': "1:200715322436:web:3f1ca4bf2ca28049e06811",
    'measurementId': "G-GSPZJ4MZH7"
}

firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
database = firebase.database()

### TESTS


def iconex(request):
    return render(request, join('core', 'iconex_test.html'))


from django.contrib.auth.models import User


def createUsers(request):
    user = User.objects.create_user('Nelson', 'wangnelson3@gmail.com',
                                    'darkarior448')
    user.save()
    messages.add_message(request, messages.WARNING, 'User created')
    return HttpResponseRedirect(reverse('index'))


### Blockchain
def addChampionToDB(firebase_id, token_id, champType):

    champion_data = { "token_id": token_id , "status": "ACTIVE", "type": champType, "firebase_account_id": firebase_id, "experience": 0, "equipment": "{}"}
    database.child("champions").child(token_id).child("details").set(champion_data)

def add_token_to_player(request):
    # Creates a token. This is sent to the player  when this is called

    return render(request, join('core', 'login.html'))

def temporal_method(request):
    #write your temporal method here


    return render(request, join('core', 'login.html'))

def add_token_test(request):
    # Withouth all the mapping fusiness. This just min  ts the token and show it up 

    #Connect to Federico wallet Method

    node_uri = "https://bicon.net.solidwallet.io/api/v3"
    network_id = 3
    hello_world_address = "cx2a96ae73368ee622f29ea6df5a9e621059326feb"
    keystore_path = "./walletFEDEKEYSTORE.119Z--hx8bad34f951350f2805af083b50562529241c5baf"
    keystore_pw = "Darkarior448!"

    wallet = KeyWallet.load(keystore_path, keystore_pw)
    tester_addr = wallet.get_address()
    icon_service = IconService(HTTPProvider(node_uri))

    #Checking the wallet data

    print("address: ", wallet.get_address()) # Returns an address
    print("private key: ", wallet.get_private_key()) # Returns a private key

    

    tester_addr = wallet.get_address()
    icon_service = IconService(HTTPProvider(node_uri))
    service_adress = "cx312f84fa11a0d315ea4331c5e601d3c4897575f8"
    # TODO Here put the receiver address from the current logged in data
    receiver_address = tester_addr

    # Way to large
    # tokenId = uuid.uuid1().int

    tokenId_start = int(str(uuid.uuid1().int)[:5])
    tokenId = tokenId_start+int(round(time.time() * 1000))

    firebase_id = request.session['local_id']
    champType = 1

    addChampionToDB(firebase_id, tokenId, champType)


    params = { '_to': receiver_address, '_tokenId': tokenId,   }

    transaction = CallTransactionBuilder().from_(tester_addr)\
                        .to(service_adress)\
                        .method("mint")\
                        .nid(3)\
                        .nonce(100)\
                        .params(params)\
                        .step_limit(1000000)\
                        .build()


    # Returns the signed transaction object having a signature
    signed_transaction = SignedTransaction(transaction, wallet)

    # Sends the transaction
    tx_hash = icon_service.send_transaction(signed_transaction)
    print(tx_hash)

    context={'newChampionName':"example"}
    return render(request, join('core', 'champion_added.html'), context)




### COMMON


def index(request):
    return render(request, join('core', 'welcome.html'))


def about(request):
    return render(request, join('core', 'about.html'))


### NOT LOGED IN


def login_page(request):

    return render(request, join('core', 'login.html'))


def signup(request):

    return render(request, join('core', 'signup.html'))


def post_login(request):

    from django.contrib.auth.models import User

    email = request.POST.get('email')
    password = request.POST.get('password')

    # # Test
    # email = 'wangnelson2@gmail.com'
    # password = 'darkarior448'

    # lazy query
    try:
        user_query = User.objects.get(email=email)
    except:
        messages.add_message(request,
                             messages.WARNING,
                             'Invalid credentials (django mail not found) %s' %
                             email,
                             fail_silently=True)
        return HttpResponseRedirect(reverse('login'))

    try:
        user_firebase = firebase_auth.sign_in_with_email_and_password(email, password)

    except:

        messages.add_message(request,
                             messages.WARNING,
                             'Invalid credentials for %s' % email,
                             fail_silently=True)
        return HttpResponseRedirect(reverse('login'))

    try:
        django_username = user_query.username
        django_user = authenticate(request,
                                   username=django_username,
                                   password=password)

        if django_user is not None:
            login(request, django_user)
        else:
            messages.add_message(
                request, messages.WARNING,
                'Actually not logged in because of django auth')

        print(user_firebase)
    except:

        messages.add_message(request,
                             messages.WARNING,
                             'You were already loged in as %s' % email,
                             fail_silently=True)
        return HttpResponseRedirect(reverse('profile'))
    name = django_username


    afterloggingin_setup(request, user_firebase)

    # request.session['address'] = str()
    messages.add_message(request, messages.SUCCESS, 'Welcome %s' % name)
    return HttpResponseRedirect(reverse('profile'))

def afterloggingin_setup(request, user_firebase):
    #TODO repeat this code in signup, bad practice but whaatever
    session_id = user_firebase['idToken']
    local_id = user_firebase['localId']

    request.session['uid'] = str(session_id)
    request.session['local_id'] = str(local_id)

    # Gets and sets the address from firebase users db (not from authentication) to the session
    local_id = str(local_id)
    # NOTE change this by actual from the authentication? by commenting the following
    # examplelocal_id = "sUB3hTuxHZZSTcdkAuopOLT8vcv2"
    # local_id = examplelocal_id

    ICX_address = database.child("users").child(local_id).child("details").child("icx_address").get().val()
    print("address: "+str(ICX_address))
    request.session['ICX_address'] = str(ICX_address)


def post_signup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    icx_address = request.POST.get('icx_address', None)


    # Create it on the django database also.
    new_user = User.objects.create_user(name, email, password)
    new_user.save()
    messages.add_message(request, messages.SUCCESS, 'Account created')
    new_user_auth = authenticate(request, username=name, password=password)
    login(request, new_user_auth)

    if (icx_address is None):
        messages.add_message(request, messages.WARNING,
                             'Remember to choose a wallet.')
        return HttpResponseRedirect(reverse('signup'))

    try:
        user_firebase = firebase_auth.create_user_with_email_and_password(
            email, password)
        uid = user_firebase['localId']
        data = {"name": name, "status": "ACTIVE", "icx_address": icx_address}
        database.child("users").child(uid).child("details").set(data)
    except:
        messages.add_message(request, messages.WARNING,
                             'Unable to sign up. with: ' + name + ' ' + email)
        return HttpResponseRedirect(reverse('signup'))

    afterloggingin_setup(request, user_firebase)
    messages.add_message(request, messages.SUCCESS, 'Successfully signed up')
    return HttpResponseRedirect(reverse('profile'))


### LOGGED IN


class profile(LoginRequiredMixin, TemplateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = join('core', 'profile.html')


class play(LoginRequiredMixin, TemplateView):

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    template_name = join('core', 'play.html')


def logout_page(request):
    auth.logout(request)
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'You had been logged off.')
    return render(request, join('core', 'welcome.html'))


### LEGACY

application_templates = {
    "volunteer": join('get_involved', 'volunteer.html'),
    "tutor": join('get_involved', 'tutor.html'),
    "ambassador": join('get_involved', 'ambassadors.html')
}


def application_view(request, application_type):

    return render(request, application_templates[application_type])


def get_involved_view(request):
    return render(request, join('get_involved', 'get_involved.html'))
