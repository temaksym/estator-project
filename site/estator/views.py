from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib import messages
from django.urls import resolve, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Property, Application
from django.utils import timezone


def property_list(request):
    properties = Property.objects.all()
    for property in properties:
        if property.images:
            property.images = property.images.split('|')[0]
    return render(request, 'property_list.html', {'properties': properties})


def property_detail_ajax(request, property_id):
    property = Property.objects.get(id=property_id)
    data = {
        'title': property.title,
        'description': property.description,
        'price': property.price,
        'address': property.address,
        'area': property.area,
        'rooms': property.rooms,
        'floor': property.floor,
        'type': property.type,
        'publication_date': property.publication_date,
        'images': property.images.split('|'),  # Split the images string
    }
    return JsonResponse(data)

# ========================================================================================================

def register(request):
    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'
    return render(request, 'register.html', {'loc':report_loc,'error': ''})
    
def signup(request):

    if request.path == '/register/signup/':
        report_loc = '../signup/'
    else: report_loc = 'signup/'

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']


        try:
            User.objects.get(email=email)
            print('Email ID is already taken, returning HTTP response')
            return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. Email ID is already taken.'})
        except:
            try:
                User.objects.get(username=username)
                print('Username already taken, returning HTTP response')
                return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. Username is already taken.'})
            except:
                if ('.' not in email) or ('@' not in email):
                    print('Email address is invalid')
                    return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. Email address is invalid.'})
                elif (password1 != password):
                    print('Passwords do not match')
                    return render(request, 'register.html', {'loc':report_loc,'errorclass':'alert alert-danger','error': 'Sorry. Passwords do not match.'})
                else:
                    User.objects.create_user(username, email, password)
                    messages.success(request, 'You succesfuly registered a new account!')
                    return redirect("../../login")

# ======================================================================================================== 

def login(request):
    print('Login Page Opened!')
    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else: report_loc = 'signin/'
    return render(request, 'login.html', {'loc':report_loc,'error': ''})


def signin(request):

    if request.path == '/login/signin/':
        report_loc = '../signin/'
    else: report_loc = 'signin/'

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect("../../")
        else:
            return redirect("../")
    else:
        return render(request, 'login.html')
    
# ========================================================================================================

def logout(request):
    logout_auth(request)
    return redirect("../../")

# ========================================================================================================

def profile(request):
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'profile.html', {'applications': applications})


def create_application(request):
    if request.method == 'POST':
        applicant = User.objects.get(id=request.POST['applicant_id'])
        property = Property.objects.get(id=request.POST['property_id'])

        application = Application(
            applicant=applicant,
            property=property,
            status="Pending",
            application_date=timezone.now(),
            message="I am interested in this property. Please contact me."
        )
        application.save()
        return redirect('profile')


def delete_application(request, application_id):
    if request.method == 'POST':
        application = Application.objects.get(id=application_id)
        application.delete()
    return redirect('profile')
    