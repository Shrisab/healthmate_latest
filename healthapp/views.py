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
from .forms import ProfileForm
import json
from healthapp import models, forms


# Create your views here.


def index(request):
    return render(request, 'healthapp/index.html')


def profile_view(request):
    return render(request, 'healthapp/profile_view.html')


@login_required(login_url='/login/')
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated.')
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'healthapp/profile_update.html', context)


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


@login_required(login_url='/login/')
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
        Consultationform = consultationform(
            name=name, email=email, phone=phone, department=department, date=date, time=time, city=city, state=state)
        Consultationform.save()
        messages.success(
            request, " Your Response is well received.We will reach you ASAP")
        # return HttpResponse('Thank you for filling appointment.We will reach you ASAP')
        mydict = {'name': name}
        appoint_template = 'healthapp/email_appointment.html'
        appoint_message = render_to_string(appoint_template, context=mydict)
        subject = 'Thank You for filling form'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, appoint_message,
                               email_from, recipient_list)
        message.content_subtype = 'html'
        message.send()
        return redirect("/")
    return render(request, "healthapp/consultationform.html")


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
            messages.warning(
                request, " Your user name must be under 10 characters")
            return redirect("/")

        if not username.isalnum():
            messages.warning(
                request, " User name should only contain letters and numbers")
            return redirect("/")
        if (pass1 != pass2):
            messages.warning(request, " Passwords do not match")
            return redirect("/")
        if User.objects.filter(username=username).exists():
            messages.warning(request, " User name already exists")
            return redirect("/")

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # end of create user
        mydict = {'username': username}
        myuser.save()
        messages.success(request, " User has been successfully created")
        html_template = 'healthapp/email_template.html'
        html_message = render_to_string(html_template, context=mydict)
        subject = 'Welcome to HealthMate'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = EmailMessage(subject, html_message,
                               email_from, recipient_list)
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

        user = authenticate(username=loginusername,
                            email=loginemail, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")

    return render(request, 'healthapp/login.html')


def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("/")


# ------------------- Blog Blog Blog ----------------------

def blog_home(request):
    context = context_data()
    posts = models.Post.objects.filter(status = 1).order_by('-date_created').all()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['latest_top'] = posts[:2]
    context['latest_bottom'] = posts[2:12]
    print(posts)
    return render(request, 'blog/blog_home.html', context)

def context_data():
    context = {
        'site_name': 'Healthmate',
        'page' : 'Blog',
        'page_title' : 'HealthBlog',
       
    }
    return context


def view_post(request, pk=None):
    context = context_data()
    post = models.Post.objects.get(id=pk)
    context['page'] = 'post'
    context['page_title'] = post.title
    context['post'] = post
    context['latest'] = models.Post.objects.exclude(id=pk).filter(
        status=1).order_by('-date_created').all()[:10]
    context['actions'] = False
    if request.user.is_superuser or request.user.id == post.user.id:
        context['actions'] = True
    return render(request, 'blog/single_post.html', context)


# def save_comment(request):
#     bannedwords = ["me", "you"]
#     resp = {'status': 'failed', 'msg': '', 'id': None}
#     if request.method == 'POST':
#         if request.POST['id'] == '':
#             form = forms.saveComment(request.POST)
#         else:
#             comment = models.Comment.objects.get(id=request.POST['id'])
#             form = forms.saveComment(request.POST, instance=comment)

#         posted_comment = request.POST["message"]
#         # for item in bannedwords:
#         #     if item in posted_comment:

#         #         return render(request, 'profile.html')

#         if form.is_valid():
#             form.save()
#             if request.POST['id'] == '':
#                 commentID = models.Post.objects.all().last().id
#             else:
#                 commentID = request.POST['id']
#             resp['id'] = commentID
#             resp['status'] = 'success'
#             messages.success(request, "Comment has been saved successfully.")
#         else:
#             for field in form:
#                 for error in field.errors:
#                     if not resp['msg'] == '':
#                         resp['msg'] += str('<br />')
#                     resp['msg'] += str(f"[{field.label}] {error}")

#     else:
#         resp['msg'] = "Request has no data sent."
#     return HttpResponse(json.dumps(resp), content_type="application/json")


# @login_required
# def delete_comment(request, pk=None):
#     resp = {'status': 'failed', 'msg': ''}
#     if pk is None:
#         resp['msg'] = 'Comment ID is Invalid'
#         return HttpResponse(json.dumps(resp), content_type="application/json")
#     try:
#         comment = models.Comment.objects.get(id=pk)
#         comment.delete()
#         messages.success(request, "Comment has been deleted successfully.")
#         resp['status'] = 'success'
#     except:
#         resp['msg'] = 'Comment ID is Invalid'

#     return HttpResponse(json.dumps(resp), content_type="application/json")
