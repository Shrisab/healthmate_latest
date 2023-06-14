from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import doctor
from .models import consultationform
from math import ceil
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,  login, logout
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



# Create your views here.


def index(request):
    return render(request, 'healthapp/index.html')

def ourservices(request):
    return render(request, 'healthapp/ourservices.html')


def about(request):
    return render(request, 'healthapp/about.html')


def ourdoctors(request):
    allDocs = []
    departdocs = doctor.objects.values('department', 'id')
    cats = {item['department'] for item in departdocs}
    for cat in cats:
        doc = doctor.objects.filter(department=cat)
        n = len(doc)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allDocs.append([doc, range(1, nSlides), nSlides])
    params = {'allDocs': allDocs}
    return render(request, 'healthapp/ourdoctors.html', params)

def Consultationform(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        department = request.POST.get('department', '')
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        # print(name,email,phone,department,date,time,city,state)
        Consultationform = consultationform( name=name, email=email, phone=phone, department=department, date=date, time=time, city=city, state=state)
        Consultationform.save()
        messages.success(request," Your Response is well received.We will reach you ASAP")
        # return HttpResponse('Thank you for filling appointment.We will reach you ASAP')
        mydict = {'name': name}
        appoint_template='healthapp/email_appointment.html'
        appoint_message=render_to_string(appoint_template,context=mydict)
        subject='Thank You for filling form'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, appoint_message, email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return redirect("/")
    return render(request,"healthapp/consultationform.html")


def blog(request):
    return render(request, 'healthapp/blog.html')


def docview(request, myid):
    # Fetching using id
    doc = doctor.objects.filter(id=myid)

    return render(request, 'healthapp/docview.html', {'doctors': doc[0]})


#  SIGNUP SECTION
def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        if len(username) > 10:
            messages.warning(request," Your user name must be under 10 characters")
            return redirect("/")

        if not username.isalnum():
            messages.warning( request," User name should only contain letters and numbers")
            return redirect("/")
        if (pass1 != pass2):
            messages.warning(request," Passwords do not match")
            return redirect("/")
        if User.objects.filter (username=username).exists():
            messages.warning(request," User name already exists")
            return redirect("/")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # end of create user 
        mydict = {'username': username}
        myuser.save()
        messages.success(request, " User has been successfully created")
        html_template='healthapp/email_template.html'
        html_message=render_to_string(html_template,context=mydict)
        subject='Welcome to HealthMate'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message, email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return redirect("/")

    else:
        return HttpResponse("404 - Not found")

    # Login section


def handleLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,email=loginemail, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return HttpResponse("404- Not found")


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("/")
