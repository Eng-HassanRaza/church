import calendar
import csv
import io

from itertools import chain

from datetime import date, datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.core import mail
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage, BadHeaderError
from django.db.models import Count, Value as V
from django.db.models import OuterRef, Subquery, Prefetch
from django.db.models.functions import Concat
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
#from easy_pdf.views import PDFTemplateView
from  django.shortcuts  import  render
from  django.views.generic  import  TemplateView

# from  config.settings  import  STRIPE_PUBLISHABLE_KEY ,  STRIPE_SECRET_KEY ,  BASE_DIR
from django.conf import settings
import  stripe
import  time
import  os

User = get_user_model()

from .models import Registration, Attendance, Members, Minutes, Church, PrayerRequest, Course, Accounts

from study.models import VerseStudyEntry

from .filters import (
    MemberFilter,
    MinutesFilter,
    ChurchFilter,
    PrayerFilter,
    CourseFilter,
    RegistrationFilter,
    AttendanceFilter,
    UserFilter,
)

from .forms import (
   MembersModelForm,
   MinutesModelForm,
   ChurchModelForm,
   SendMessageForm,
   RequestAccountForm,
   RequestChurchInformation,
   PrayerRequestModelForm,
   PrayerCircleForm,
   EditUserModelForm,
   CourseModelForm,
   RegistrationForm,
   AttendanceModelForm,
   AnonPrayerRequestForm,
   AttendanceCourseForm,
   UserModelForm,
   AccountsModelForm,
   EnterContributionsForm,
   PaymentDetailForm,
   BankDetailForm,
)

def accounting_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "accounting_information.html", {})

def minutes_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "minutes-information.html", {})

def member_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "member-information.html", {})

def contribution_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "contribution-information.html", {})

def course_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "event-information.html", {})

def attendance_information(request):
    my_title = ""
    context = {"title": my_title}
    return render(request, "attendance-information.html", {})

def home_page(request):
    my_title = "Home Page"
    context = {"title": my_title}
    return render(request, "home.html", {})

@csrf_exempt
def user_login(request):
    # form =  LoginForm(request)
    # render_to_response('login.html')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        #print("befor login")
        #print(request)
        user = authenticate(request, username=username, password=password)
        #print("afer login")
        #print(user)
        if user is not None:
            login(request, user)
            if user.is_active:
                return HttpResponseRedirect("/")
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid Login Credentials,  <a href='/login'>Try Again</>")
    return render(request, "login.html", {})


def user_logout(request):
    logout(request)
    return HttpResponse("<a href='/login'><h2>Log  In</></h2>")

def divide_chunks(l, n):
    n = 50
    for i in range(0, len(l), n):
        yield l[i:i + n]

def send_email_to_members (request):
    if request.method == 'POST':
        form = SendMessageForm(request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message_text = form.cleaned_data["message"]
            user = User.objects.filter(is_active=True, church=request.user.church, groups__name="Member")
            emailto = [user.email for user in user]
            from_email=settings.DEFAULT_FROM_EMAIL
            chunks=divide_chunks(emailto, 50)
            for chunk in chunks:
                n=50
                mail = EmailMultiAlternatives(subject, message_text,from_email, [], bcc=chunk)
                mail.send()
            return redirect('/')
        else:
            return HttpResponse('Something went wrong.  Please click Back on your browser to try again.')
    else:
        form = SendMessageForm()
    template_name = "form.html"
    context = {"form": form, "title": "Email all Members"}
    return render(request, template_name, context)

def request_account_view(request):
    if request.method == 'POST':
        form = RequestAccountForm(request.POST)
        if form.is_valid():
            your_church = form.cleaned_data['your_church']
            username_requested = form.cleaned_data['username_requested']
            password_requested = form.cleaned_data['password_requested']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']            
            from_email = form.cleaned_data['from_email']
            phone = form.cleaned_data['phone']
            emailto = [form.cleaned_data["your_church"].email]
            send_mail(
            "Account Setup Requested",
            "Username Requested: {0}\nPassword Requested: {1}\nTheir email: {4}\nFirst Name: {2}\nLast Name: {3}\nPhone: {5}\n\nIt is at your discretion if you allow this user to have a login associated with your church.\n\nLog-ins do NOT provide users access to any church information.  You will have the option to add this user to your Members list.  Creating a user account only links the user with your church and allows them to submit an offering or be on the leaderboard for verse practices.\n\nIf the username already exists or the password does not meet requirements, alter them accordingly and make sure that you send a confirmation email to this person and include that information.\n\nExample:  Welcome to (list your church)! \nYou now have a personal login.  Your username is: (username)\nYour password is: (password).\n\nThe user will receive no information automatically.".format(
            form.cleaned_data['username_requested'],
            form.cleaned_data["password_requested"], 
            form.cleaned_data["first_name"],                 
            form.cleaned_data["last_name"],
            form.cleaned_data["from_email"],
            form.cleaned_data["phone"],
            ),
            from_email,
            emailto,
            fail_silently=True,
            )
            return HttpResponse('Your request was submitted.  Feel free to contact the church directly.')
        else:
            print (form.errors)
    else:
        form = RequestAccountForm()
    my_title = "Request A User Account"
    template_name = "request_account_view_template.html"
    context =  {"title":my_title, "form": form}
    return render(request, template_name, context)

def request_church_account_view(request):
    if request.method == 'POST':
        form = RequestChurchInformation(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            church_name = form.cleaned_data['church_name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']       
            emailto = ["tynercreeksoftware@gmail.com"]
            from_email=form.cleaned_data["email"]
            send_mail(
            "Information for New Church Requested",
            "Name: {0}\nPhone: {1}\nChurch Name: {2}\nMessage: {3}\nEmail: {4}".format(
            form.cleaned_data['name'],
            form.cleaned_data["phone"], 
            form.cleaned_data["church_name"],                 
            form.cleaned_data["message"],
            form.cleaned_data["email"],
            ),
            from_email,
            emailto,
            fail_silently=True,
            )
            return HttpResponse('Your request was submitted.  Feel free to contact us directly at tynercreeksoftware@gmail.com or (405) 578-5701.')
        else:
            print (form.errors)
    else:
        form = RequestChurchInformation()
    my_title = "Request Information for Your Church"
    template_name = "request_church_account_view_template.html"
    context =  {"title":my_title, "form": form}
    return render(request, template_name, context)

def prayer_request_anon_create_view(request):
    if request.method == 'POST':
        form = AnonPrayerRequestForm(request.POST)
        if form.is_valid():
            person = form.cleaned_data['person']
            author = form.cleaned_data['author']
            prayer = form.cleaned_data['prayer']
            phone = form.cleaned_data['phone']
            church = form.cleaned_data['church']
            from_email = 'thechurchsite.net@gmail.com',
            send_mail(
            "Prayer Requested",
            "Pray For: {0}\n{1}\n\nRequested By: {2}, Phone: {3}".format(
            form.cleaned_data['person'],
            form.cleaned_data["prayer"],
            form.cleaned_data["author"],
            form.cleaned_data["phone"],
            ),
            'thechurchsite.net@gmail.com',
            [church.email],
            fail_silently=True,
            )
            return HttpResponse('We will be praying for you.')
        else:
            print (form.errors)
    else:
            form = AnonPrayerRequestForm()
    my_title = "Request Prayer"
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def attendance_list_view(request):
    my_title = "Your Attendance"
    qs = Attendance.objects.all()
    attendance_filter = AttendanceFilter(request.GET, queryset=qs)
    template_name = "attendance_list_view.html"
    context = {"object_list": attendance_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def attendance_report_event_view(request):
    my_title = "Attendance Report"
    church = request.user.church
    course_counts = Attendance.objects.values("course").annotate(Count("present")).order_by()
    attendance_list = Attendance.objects.order_by('attendance_date').filter(course__church=church)
    qs = Attendance.objects.distinct('course').order_by('course')
    attendance_filter = AttendanceFilter(request.GET, queryset=qs)
    template_name = "attendance_report_event_inline.html"
    context = {'course_counts':course_counts, 'attendance_list': attendance_list, "object_list": attendance_filter, "title": my_title}
    print (course_counts)
    return render(request, template_name, context)

@login_required
def registration_admin_schedule_view(request):
    my_title = "Church Registrations"
    registration_list = Registration.objects.all()
    course_counts = Registration.objects.values("course").annotate(Count("member")).order_by()
    qs = Registration.objects.distinct('course').order_by('course')
    registration_filter = RegistrationFilter(request.GET, queryset=qs)
    template_name = "registration_admin_schedule_view.html"
    context = {'course_counts':course_counts,'registration_list':registration_list, "object_list": registration_filter, "title": my_title}
    print (course_counts)
    return render(request, template_name, context)

@login_required
def accounts_create_view(request):
    my_title = "Set Up an Account"
    form = AccountsModelForm(request.POST or None)
    id = request.user.church.id
    form.fields['church'].queryset = Church.objects.filter(id=id)
    if form.is_valid():
        form.save()
        form = AccountsModelForm()
        return redirect("/accounts")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)



@login_required
def accounts_update_view(request, id=None):
    church=request.user.church
    obj = get_object_or_404(Accounts, church=church)
    form = AccountsModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        form = AccountsModelForm()
        return redirect("/accounts")
    template_name = "form.html"
    context = {"title": f"Update {obj.name}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def accounts_delete_view(request, id):
    obj = get_object_or_404(Accounts, id=id)
    template_name = "accounts_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/accounts")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def accounts_detail_page(request, id):
    obj = Accounts.objects.get(id=id)
    template_name = "accounts_detail_page.html"
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def accounts_list_view(request):
    my_title = "Accounts"
    church = request.user.church
    qs = Accounts.objects.filter(church=church)
    template_name = "accounts_list_view.html"
    context = {"object_list": qs, "title": my_title}
    return render(request, template_name, context)







@login_required
def attendance_report_date_view(request):
    my_title = "Attendance Report"
    church = request.user.church
    course_counts = Attendance.objects.values("attendance_date").annotate(Count("present")).order_by()
    attendance_list = Attendance.objects.order_by('attendance_date').filter(course__church=church)
    qs = Attendance.objects.distinct('attendance_date').order_by('attendance_date')
    attendance_filter = AttendanceFilter(request.GET, queryset=qs)
    template_name = "attendance_report_date_inline.html"
    context = {'course_counts':course_counts, 'attendance_list': attendance_list, "object_list": attendance_filter, "title": my_title}
    print (course_counts)
    return render(request, template_name, context)

@login_required
def attendance_report_student_view(request):
    my_title = "Attendance Report"
    church = request.user.church
    course_counts = Attendance.objects.values("student").annotate(Count("present")).order_by()
    attendance_list = Attendance.objects.order_by('attendance_date').filter(course__church=church)
    qs = Attendance.objects.distinct('student').order_by('student')
    attendance_filter = AttendanceFilter(request.GET, queryset=qs)
    template_name = "attendance_report_student_inline.html"
    context = {'course_counts': course_counts, 'attendance_list': attendance_list, "object_list": attendance_filter, "title": my_title}
    print (course_counts)
    return render(request, template_name, context)


@login_required
def administrator_attendance_list_view(request):
    my_title = "Church Attendance"
    qs = Attendance.objects.all()
    attendance_filter = AttendanceFilter(request.GET, queryset=qs)
    template_name = "administrator_attendance_list_view.html"
    context = {"object_list": attendance_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def check_in_view(request):
    my_title = "Check In"
    form = AttendanceModelForm(request.POST or None)
    id=request.user.id
    church=request.user.church
    form.fields['student'].queryset = User.objects.filter(id=id)
    attendee =  request.user.id
    form.fields['course'].queryset = Course.objects.filter(church=church)
    if form.is_valid():
        form.save()
        form = AttendanceModelForm()
        return redirect("/")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def attendance_create_view(request):
    my_title = "Record Attendance"
    form = AttendanceModelForm(request.POST or None)
    form.fields['student'].queryset = User.objects.filter(church=request.user.church)
    form.fields['course'].queryset = Course.objects.filter(church=request.user.church)
    form.fields['present']="True"
    if form.is_valid():
        form.save()
        form = AttendanceModelForm()
        return redirect("/attendance")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def record_attendance_choose_course_view(request):
    course_id=""
    my_title = "Record Attendance - Select Event For Which You Would Like To Record Attendance."
    if request.POST:
        form = AttendanceCourseForm(request.POST, request=request)
        if form.is_valid():
            course_id=form.cleaned_data.get('course')
            return HttpResponseRedirect("/attendance-record/{}/".format(form.cleaned_data["course"].id))
    else:
        form = AttendanceCourseForm(request=request)
    
    template_name = "record_attendance.html"
    context = {"form": form, "title": my_title,'course_id':course_id}
    return render(request, template_name, context)

@login_required
def record_attendance_view(request, course_id):
    my_title = "Record Attendance"
    atten=[]
    students = User.objects.filter(church = request.user.church)
    course = get_object_or_404(Course, id=course_id)
    context = {"title": my_title,'course_id':course_id,'students':students }
    
    if request.method == 'POST':
        date_data = request.POST.get('attendance_date','')
        valid = True
        try:
            attendance_date = datetime.strptime(date_data, '%m/%d/%Y')
        except Exception as e:
            valid = False
            messages.error(request, "Can not convert date: %s" % date_data)

        if valid:
            for student in students: 
                do_present = request.POST.get('present_' + str(student.pk), '')
                if do_present == 'Present':
                    present = True
                else: 
                    present = False

                try:
                    attendance_obj = Attendance.objects.get(
                            course = course,
                            student = student,
                            attendance_date = attendance_date)
                except Attendance.DoesNotExist:
                    attendance_obj = Attendance.objects.create(
                        course = course,
                        student = student,
                        attendance_date = attendance_date,
                        present=present)

                attendance_obj.present = present
                attendance_obj.save()

                context ['successMsg'] = 'Attendance recorded successfully.'
            return redirect("/attendance/")
            
    context ['atten'] = atten   
    template_name = "record_attendance.html"
    return render(request, template_name, context)

@login_required
def attendance_update_view(request, id=None):
    obj = get_object_or_404(Attendance, id=id)
    form = AttendanceModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.cleaned_data["email"] = form.cleaned_data["email"].lower()
        form.save()
        form = AttendanceModelForm()
        return redirect("/attendance")
    template_name = "form.html"
    context = {"title": f"Update {obj.first_name} {obj.last_name}", "form": form}
    return render(request, template_name, context)

@login_required
def attendance_delete_view(request, id):
    obj = get_object_or_404(Attendance, id=id)
    template_name = "attendance_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/attendance")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def attendance_detail_page(request, id):
    obj = Attendance.objects.get(id=id)
    template_name = "attendance_detail_page.html"
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def church_create_view(request):
    my_title = "Set Up a Church"
    form = ChurchModelForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ChurchModelForm()
        return redirect("/church")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def church_update_view(request, id=None):
    id=request.user.church.id
    obj = get_object_or_404(Church, id=id)
    form = ChurchModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        form = ChurchModelForm()
        return redirect("/church")
    template_name = "form.html"
    context = {"title": f"Update {obj.name}", "form": form}
    return render(request, template_name, context)

@login_required
def church_delete_view(request, id):
    obj = get_object_or_404(Church, id=id)
    template_name = "church_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/church")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def church_detail_page(request, id):
    obj = Church.objects.get(id=id)
    template_name = "church_detail_view.html"
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def church_list_view(request):
    my_title = "Churches"
    id = request.user.church.id
    qs = Church.objects.filter(id=id)
    church_filter = ChurchFilter(request.GET, queryset=qs)
    template_name = "church_list_view.html"
    context = {"object_list": church_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def member_create_view(request):
    my_title = "Add a Member (Must have an Account)"
    #MembersModelForm.base_fields['user'] = User.objects.filter(church=request.user.church)
    form = MembersModelForm(request.POST or None)
    form.fields['user'].queryset = User.objects.exclude(groups__name="Member").filter(church=request.user.church)
    if form.is_valid():
        form.save()
        group = Group.objects.get(name='Member')
        user = form.cleaned_data["user"]
        user.groups.add(group)
        form = MembersModelForm()
        return redirect("/members")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def user_create_view(request):
    my_title = "Add a New User Account"
    form = UserModelForm(request.POST or None)
    id = request.user.church.id
    form.fields['church'].queryset = Church.objects.filter(id=id)
    if form.is_valid():
        form.cleaned_data["email"] = form.cleaned_data["email"].lower()
        form.save()
        form = UserModelForm()
        return redirect("/users")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def user_update_view(request, id=None):
    obj = get_object_or_404(User, id=id)
    form = EditUserModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.cleaned_data["email"] = form.cleaned_data["email"].lower()
        form.save()
        form = EditUserModelForm()
        return redirect("/users")
    template_name = "form.html"
    context = {"title": f"Update {obj.first_name} {obj.last_name}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def user_delete_view(request, id):
    obj = get_object_or_404(User, id=id)
    template_name = "user_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/users")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def user_list_view(request):
    my_title = "Your Users"
    qs = User.objects.filter(church=request.user.church).order_by("last_name")
    user_filter = UserFilter(request.GET, queryset=qs)
    template_name = "user_list_view.html"
    context = {"object_list": user_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def download_user_list(request):
    response = HttpResponse(content_type='users/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    writer = csv.writer(response)
    writer.writerow(['first_name','last_name','email','street_address','street_address_line_2','city','state_abbrev','zip_code','phone_number'])
    church=request.user.church
    users = User.objects.filter(church = church).values_list('first_name','last_name','email','street_address','street_address_line_2','city','state_abbrev','zip_code','phone_number')
    for user in users:
        writer.writerow(user)
    return response

def clear_field(content):
    if content:
        return content.strip()
    return ""

@login_required
def user_upload(request):
    template = "user_upload.html"
    prompt = {
        'order': "The columns should be: Username, Password, First Name, Last Name, Street Address, Street Address Line 2, City, State Abbreviation, Zip, Phone Number, Email"
    }
    
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, "Only CSV files may be uploaded.")
        return render(request, template)

    data_set = ""
    try:
        data_set = csv_file.read().decode("UTF8")
    except Exception as e:
        csv_file.seek(0)
        data_set = csv_file.read().decode("ISO-8859-1")

    io_string = io.StringIO(data_set)

    # header count check
    header = next(io_string)
    header_clean = [x for x in header.split(',') if not x in ['', '\r\n', '\n']]
    if len(header_clean) != 11:
        messages.error(request, "Make sure table consists of 11 columns. %s" % prompt['order'])
        return render(request, template)

    churches : List[Church] = []
    for column in csv.reader(io_string, delimiter=',', quotechar='"'):
        if not column:
            continue
        username = clear_field(column[0])
        password = clear_field(column[1])
        first_name = clear_field(column[2])
        last_name = clear_field(column[3])
        street_address = clear_field(column[4])
        street_address_line_2 = clear_field(column[5])
        city = clear_field(column[6])
        state_abbrev = clear_field(column[7])
        zip_code = clear_field(column[8])
        phone_number = clear_field(column[9])
        email = clear_field(column[10])

        User = get_user_model()
        if User.objects.filter(username=username).count() > 0:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.save()
        else:
            user = User.objects.create_user(username, email, password)

        user.is_superuser = False
        user.is_active = True
        user.is_staff = False
        user.first_name = first_name
        user.last_name = last_name
        id = request.user.church.id

        church = Church.objects.get(id=id)
        user.church = church
        user.save()

    # # display message for each district if count >= qty
    # for district in districts:
    #     users_in_district_count = district.user_set.filter(is_active=True).count()
    #     if users_in_district_count >= district.user_license_qty:
    #         messages.warning(request, f"The number of active users for {district.name} is now: {users_in_district_count}. The district has a license for {district.user_license_qty}")

    return redirect("/")

@login_required
def member_list_view(request):
    my_title = "Members"
    qs = User.objects.filter(groups__name="Member", church=request.user.church).order_by("last_name")
    member_filter = MemberFilter(request.GET, queryset=qs)
    template_name = "member_list_view.html"
    context = {"object_list": member_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def download_member_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'
    writer = csv.writer(response)
    writer.writerow(['first_name','last_name','email','street_address','street_address_line_2','city','state_abbrev','zip_code','phone_number'])
    church=request.user.church
    members = User.objects.filter(groups__name="Member", church = church).values_list('first_name','last_name','email','street_address','street_address_line_2','city','state_abbrev','zip_code','phone_number')
    for member in members:
        writer.writerow(member)
    return response

@login_required
def minutes_create_view(request):
    my_title = "Enter Minutes"
    form = MinutesModelForm(request.POST or None)
    id = request.user.id
    form.fields['recorder'].queryset = User.objects.filter(id=id, groups__name="Member")
    if form.is_valid():
        form.save()
        form = MinutesModelForm()
        return redirect("/minutes")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def minutes_update_view(request, id=None):
    obj = get_object_or_404(Minutes, id=id)
    form = MinutesModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        form = MinutesModelForm()
        return redirect("/minutes")
    template_name = "form.html"
    context = {"title": f"Update {obj.meeting_date}", "form": form}
    return render(request, template_name, context)

@staff_member_required
def minutes_delete_view(request, id):
    obj = get_object_or_404(Minutes, id=id)
    template_name = "minutes_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/minutes")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def minutes_detail_page(request, id):
    obj = Minutes.objects.get(id=id)
    template_name = "minutes_detail_view.html"
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def minutes_list_view(request):
    my_title = "Minutes"
    qs = Minutes.objects.all()
    minutes_filter = MinutesFilter(request.GET, queryset=qs)
    template_name = "minutes_list_view.html"
    context = {"object_list": minutes_filter, "title": my_title}
    return render(request, template_name, context)

# class MinutesPDFView(PDFTemplateView):
#     template_name = 'minutes_detail_view.html'

def prayer_request_create_view(request):
    my_title = "Request Prayer"
    form = PrayerRequestModelForm(request.POST or None)
    id = request.user.id
    church_id=request.user.church.id
    form.fields['church'].queryset = Church.objects.filter(id=church_id)
    form.fields['author'].queryset = User.objects.filter(id=id)
    if form.is_valid():
        form.save()
        form = PrayerRequestModelForm()
        return redirect("/prayer")
    template_name = "form.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

def prayer_request_list_view(request):
    my_title = "Prayer Requests"
    qs = PrayerRequest.objects.all()
    prayer_filter = PrayerFilter(request.GET, queryset=qs)
    template_name = "prayer_request_view.html"
    context = {"object_list": prayer_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def prayer_update_view(request, id=None):
    obj = get_object_or_404(PrayerRequest, id=id)
    form = PrayerRequestModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        form = PrayerRequestModelForm()
        return redirect("/prayer")
    template_name = "form.html"
    context = {"title": "Update Prayer Request", "form": form}
    return render(request, template_name, context)

@staff_member_required
def prayer_delete_view(request, id):
    obj = get_object_or_404(PrayerRequest, id=id)
    template_name = "prayer_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/prayer")
    context = {"object": obj}
    return render(request, template_name, context)

def activate_prayer_circle (request):
    if request.method == 'POST':
        form = PrayerCircleForm(request.POST or None)
        if form.is_valid():
            prayer = form.cleaned_data["prayer"]
            subject = "Please Start the Prayer Circle"
            church = request.user.church
            user = User.objects.filter(church=church)
            #Course.objects.filter( course_teacher__email__contains=request.user.email):
            emailto = [user.email for user in user]
            mail= EmailMessage(
                subject = "Please Start the Prayer Circle",
                body = prayer,
                from_email = 'thechurchsite.net@gmail.com',
                to = emailto,
                )
            mail.send(fail_silently=False)
            return redirect('/')
        else:
            return HttpResponse('Something went wrong.  Please click Back on your browser to try again.')
    else:
        form = PrayerCircleForm()
    template_name = "form.html"
    context = {"form": form, "title": "Activate Church Prayer Circle"}
    return render(request, template_name, context)

@login_required
def course_create_view(request):
    my_title = "Set Up a Class or Event"
    form = CourseModelForm(request.POST or None)
    form.fields['teacher'].queryset = User.objects.filter(groups__name="Member", church=request.user.church)
    form.fields['church'].queryset = Church.objects.filter(name=request.user.church.name)
    if form.is_valid():
        form.save()
        return redirect('/events')
    template_name = "course_create_view.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context)

@login_required
def course_list_view(request):
    my_title = "Classes, Meetings and Events"
    qs = Course.objects.all()
    course_filter = CourseFilter(request.GET, queryset=qs)
    template_name = "course_list_view.html"
    context = {"object_list": course_filter, "title": my_title}
    return render(request, template_name, context)

@login_required
def course_delete_view(request, id):
    obj = get_object_or_404(Course, id=id)
    template_name = "course_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/events")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def register_for_an_event_view(request):
    my_title = ("Register for an Event or Class")
    form = RegistrationForm(request.POST or None)
    id=request.user.id
    form.fields['member'].queryset = User.objects.filter(id=id)
    form.fields['course'].queryset = Course.objects.filter(church=request.user.church)
    
    if form.is_valid():
        form.save()
        return redirect ('/registration')
        form = RegistrationForm()
    template_name = "register_for_an_event_view.html"
    context = {"form": form, "title": my_title}
    return render(request, template_name, context) 
    
@login_required
def registration_delete_view(request, id):
    obj = get_object_or_404(Registration, id=id)
    template_name = "registration_delete_view.html"
    if request.method == "POST":
        obj.delete()
        return redirect("/registration")
    context = {"object": obj}
    return render(request, template_name, context)

@login_required
def registration_schedule_view(request):
    my_title = "Your Events"
    qs = Registration.objects.all()
    registration_filter = RegistrationFilter(request.GET, queryset=qs)
    template_name = "registration_schedule_view.html"
    context = {"object_list": registration_filter, "title": my_title}
    return render(request, template_name, context)







#below here is not functioning yet------

def course_update_view(request, id=None):
    obj = get_object_or_404(Course, id=id)
    form = CourseModelForm(request.POST or None, instance=obj)
    #form.fields['teacher'].queryset = User.objects.filter(groups__name="Member", church=request.user.church)
    #form.fields['church'].queryset = Church.objects.filter(name=request.user.church.name)
    if form.is_valid():
        form.save()
        return redirect("/")
    template_name = "course_update_view.html"
    context = {"object": obj, "title": f"Update {obj.course_title}", "form": form}
    return render(request, template_name, context)

@login_required
def course_detail_page(request, id):    
    obj = get_object_or_404(Course, id=id)
    qs = Course.objects.all()
    course_filter = CourseFilter(request.GET, queryset=qs)
    template_name = "course_detail_page.html"
    context = {"object": course_filter}
    return render(request, template_name, context)

@login_required
def course_roster_view(request):
    my_title = "Class Roster"
    qs = Course.objects.all()
    roster_list = CourseRosterFilter(request.GET, queryset=qs)
    template_name = "course_roster_view.html"
    context = {"object_list": roster_list, "title": my_title}
    return render(request, template_name, context)

@login_required
def contributions_enter(request):
    # list_of_users_by_church = User.objects.filter(is_active=True, church_id=request.user.church.id, groups__name="Member")
    list_of_users_by_church = User.objects.filter(is_active=True, church_id=request.user.church.id)

    form = EnterContributionsForm(request.POST or None,user=request.user)
    id = request.user.church.id
    form.fields['church'].queryset = Church.objects.filter(id=request.user.church.id)
    if form.is_valid():
        form.save()
        form = EnterContributionsForm(user=request.user)
        return redirect("/")
    template_name = "form.html"
    context = {"form": form, "title": "my_title"}
    return render(request, template_name, context)

    # template_name = "contributions-enter.html"
    # context = {"user_list": list_of_users_by_church, "title": "Enter Contribution"}
    # return render(request, template_name, context)


# stripe.api_key = "sk_live_R8lejwrvJOrZgDZDdFuFMLv900E2UUvU7h"
stripe.api_key = "sk_test_oPzX9vEJPM6dUFIMZdkZubsc002KBVt8AE"


#############################
# 商品を売る人のstripeアカウント
#############################

def create_custom_account(email):
    account = stripe.Account.create(
        type="custom",
        country="US",
        email=email,  # user email
        business_type="individual",
        capabilities={
            "card_payments": {"requested": True},
            "transfers": {"requested": True},
        },
    )
    return account


def create_account_person(user_id):
    # pserson tokenについて
    # https://stripe.com/docs/connect/account-tokens

    token = "token-person"  # request.form['token-person] 上の情報を参照
    person = stripe.Account.create_person(
        user_id,

    )


def get_custom_account(acct_id):
    account = stripe.Account.retrieve(acct_id)
    return account


def update_custom_account(acct_id,form_obj,church,base_host):
    account = get_custom_account(acct_id)
    print(account)

    # アカウント情報の更新
    res = stripe.Account.modify(
        acct_id,
        individual={
            'first_name': form_obj.first_name,
            'last_name': form_obj.last_name,
            'phone': form_obj.phone,
            'gender': form_obj.gender,  # male or female
            'email': church.email,
            'id_number': form_obj.id_number,
            'address': {
                "country": "US",
                "state": form_obj.state,
                "city": form_obj.city,
                "town": form_obj.town,
                "line1": form_obj.line1,
                "postal_code": form_obj.postal_code,
            },
            'dob': {
                "day": form_obj.date_of_birth.day,
                "month": form_obj.date_of_birth.month,
                "year": form_obj.date_of_birth.year
            },

        },
        business_profile={
            "mcc": "8661",
            "name":church.name,
            "url":base_host+"/church/"+str(church.id)
        },
        tos_acceptance={
            "date": int(time.time()),  # => 1399605420   # 経過秒数を整数で取得
            "ip": "8.8.8.8"  # グローバルIPアドレスを入力
        }
    )


def create_bank_account(acct_id,form_obj):
    # 銀行講座登録
    account = stripe.Account.create_external_account(
        acct_id,
        external_account={
            "object": "bank_account",
            "account_number": form_obj.account_number,
            # "account_number": "000123456789",
            "routing_number": form_obj.routing_number,
            # "routing_number": "110000000",
            "account_holder_name": form_obj.account_holder_name,
            # "account_holder_name": "タナカタロウ",
            "account_holder_type": "individual",
            "currency": "usd",
            "country": "US"
        }
    )


def update_payouts_schedule(acct_id):
    account = get_custom_account(acct_id)

    # 入金のスケジュールを更新
    res = stripe.Account.modify(
        acct_id,
        settings={"payouts": {"schedule": {
            "delay_days": 4,
            "interval": "weekly",
            "weekly_anchor": "friday"
        },
        }}
    )


def upload_identity_verification_file(acct_id, img_path):
    # https://stripe.com/docs/connect/identity-verification-api
    with open(img_path, "rb") as fp:
        res = stripe.FileUpload.create(
            purpose='identity_document',
            file=fp,
            stripe_account=acct_id
        )
        verification_id = res["id"]

        res = stripe.Account.modify(
            acct_id,
            individual={"verification": {
                "document": {
                    "front": verification_id
                }
            }})

        print(res)


#############################
# 商品を買う人のstripeアカウント
#############################

def create_user_account(user):
    """
    "id":"cus_FbYcVYlQhY5Yzv"
    """
    strip_customer = stripe.Customer.create(
        description=user.username,
        email=user.email
    )
    return strip_customer


def charge_user(acct_id, amount, application_fee):
    # https://stripe.com/docs/connect/direct-charges#collecting-fees
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        description='charge',
        source="tok_visa",  # request.POST['stripeToken']
        application_fee_amount=application_fee,
        stripe_account=acct_id
    )
    print(charge)


class ShopView(TemplateView):
    template_name = 'stripe_home.html'

    def get_context_data(self, **kwargs):
        context = super(ShopView, self).get_context_data(**kwargs)

        # https://stripe.com/docs/api/errors/handling #Error handling (not implemented this time)

        ####################### ###############
        # 1. Create a Custom account
        ################################ #######

        account = create_custom_account()

        ####################################
        # 2. Update account information
        ####### #############################

        CONNECTED_STRIPE_ACCOUNT_ID = account.id

        update_custom_account(CONNECTED_STRIPE_ACCOUNT_ID)

        ####################################
        # 3. Bank account registration
        ####### #############################

        create_bank_account(CONNECTED_STRIPE_ACCOUNT_ID)
        update_payouts_schedule(CONNECTED_STRIPE_ACCOUNT_ID)

        ####################################
        # 4. Proof of identity
        ######### ###########################

        image_path = os.path.join(settings.BASE_DIR, "static/images", "success.png")

        upload_identity_verification_file(CONNECTED_STRIPE_ACCOUNT_ID, image_path)

        ####################################
        # 5. Payment
        ########## ##########################

        charge_user(CONNECTED_STRIPE_ACCOUNT_ID, 5000, 500)

        return context

def charge_amount_payment(request):
    CONNECTED_STRIPE_ACCOUNT_ID = "acct_1ISIYMRG5pWu1wHn"
    charge_user(CONNECTED_STRIPE_ACCOUNT_ID, 5000, 500)

    return redirect("/")

def add_payment_details(request,id):
    church = Church.objects.filter(id=id).first()
    base_host = request.get_host()
    form = PaymentDetailForm(request.POST or None, church=church)
    form.fields['church'].queryset = Church.objects.filter(id=id)
    if form.is_valid():
        form_obj = form.save()
        church_email = church.email
        stripe_account = create_custom_account(church_email)
        ###### Initial account creation ############
        CONNECTED_STRIPE_ACCOUNT_ID = stripe_account.id
        church.stripe_id = CONNECTED_STRIPE_ACCOUNT_ID
        church.save()

        ######### Account details Updates #########

        update_custom_account(CONNECTED_STRIPE_ACCOUNT_ID,form_obj,church,base_host)
        church.payment_verified = True
        church.save()
        form = PaymentDetailForm(church=church)
        return redirect("/church/")
    template_name = "payment_details_form.html"
    context = {"form": form, "title": "my_title","church_id":id}
    return render(request, template_name, context)

def add_bank_details(request,id):
    church = Church.objects.filter(id=id).first()
    form = BankDetailForm(request.POST or None, church=church)
    form.fields['church'].queryset = Church.objects.filter(id=id)
    acct_id = church.stripe_id
    if form.is_valid():
        form_obj = form.save()
        create_bank_account(acct_id,form_obj)
        update_payouts_schedule(acct_id)
        image_path = os.path.join(settings.BASE_DIR, "static/images", "success.png")

        upload_identity_verification_file(acct_id, image_path)
        church.is_bank_verified = True
        church.save()
        form = BankDetailForm(church=church)
        return redirect("/church/")
    template_name = "bank_details_form.html"
    context = {"form": form, "title": "my_title","church_id":id}
    return render(request, template_name, context)


@login_required
def church_contribution_view(request):
    my_title = "My Churches"
    id = request.user.church.id
    qs = Church.objects.filter(id=id)
    church_filter = ChurchFilter(request.GET, queryset=qs)
    template_name = "church_contribution_list_view.html"
    context = {"object_list": church_filter, "title": my_title}
    return render(request, template_name, context)

