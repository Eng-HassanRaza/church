from django import forms
from django.forms import ModelForm, Textarea
from django.utils.safestring import mark_safe
from django.db.models import Count, F
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Identity_Verification,Registration, Attendance, Members, Minutes, Church, User, PrayerRequest, Course,Payment_Detials,Bank_Details
from .models import Accounts, FixedAssets, CurrentLiabilities,LongTermLiabilities, Income,Expense, Vendor, Customer, Transactions, AccountsPayable, AccountsReceivable,Contribution

FUNDTAG = [
    ("General Fund","General Fund"),
    ("Building Fund", "Building Fund"),
    ("Missionary","Missionary"),
    ("Special","Special"),
    ("Other","Other"),
    ]

ACCOUNTTYPE = [
    ("Checking", "Checking"), 
    ("Savings", "Savings"),
    ("Accounts Receivable", "Accounts Receivable"),
    ("Other", "Other"),
    ]

POSNEG = [
    ("Deposit", "Deposit"),
    ("Withdrawal", "Withdrawal")
    ]

ASSETTYPE = [
    ("Building", "Building"), 
    ("Equipment", "Equipment"),
    ("Vehicle", "Vehicle"),
    ("Other", "Other"),
    ]

CURRENTLIABILITYTYPE = [
    ("Credit Card", "Credit Card"), 
    ("Accounts Payable", "Accounts Payable"),
    ("Other", "Other"),
    ]

OPENORCLOSED = [
    ("Open", "Open"), 
    ("Closed", "Closed"),
    ]

LONGTERMTYPE = [
    ("Loan", "Loan"), 
    ("Other", "Other"),
    ]

INCOMETYPE = [
    ("Contribution","Contribution"),
    ("Grant","Grant"),
    ("Other","Other"),
    ]

EXPENSETYPE = [
    ("Salary","Salary"),
    ("Rent","Rent"),
    ("Bank Fee","Bank Fee"),
    ("Building Fee","Building Fee"),
    ("Office Supplies","Office Supplies"),
    ("Other","Other"),
    ]

class RequestAccountForm(forms.Form):
    your_church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    username_requested = forms.CharField(required=True, label="What would you like your username to be?")
    password_requested = forms.CharField(required=True, label="Choose a password with at least 8 characters, one of them being a special character.")
    first_name = forms.CharField(required=True, label="Your First Name")
    last_name = forms.CharField(required=True, label="Your Last Name")           
    from_email = forms.EmailField(required=True, label="Your Email")               
    phone = forms.CharField(required=True, label="Your Phone Number")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['your_church'].queryset = Church.objects.all()

class ChurchModelForm(forms.ModelForm):
    class Meta:
        model = Church
        fields = [
            "name",
            "phone_number",
            "street_address",
            "street_address_line_2",
            "city",
            "state_abbrev",
            "zip_code",
        ]
        labels = {
            "name": "Church Name",
            "phone_number": "Phone Number",
            "street_address": "Street Address - Line 1",            
            "street_address_line_2": "Street Address - Line 2",
            "city": "City",
            "state_abbrev": "Two Digit State Abbreviation",
            "zip_code": "Zip Code",
        }

class MembersModelForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('last_name').distinct())
    
    class Meta:
        model = Members
        fields = [
            "user",
        ]
        labels = {
            "user": "Choose the member.",
        }

class MinutesModelForm(forms.ModelForm):
    minutes_details = forms.CharField(widget=forms.Textarea, required=True, label="Minutes Details", max_length=20000)

    class Meta:
        model = Minutes
        fields = [
            "meeting_date",
            "minutes_details",
            "recorder",
        ]
        labels = {
            "meeting_date": "Meeting Date",
            "minutes_details": "Minutes Details",
            "recorder": "Recorder Name",
        }

class AttendanceCourseForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ["course"]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(
            church=request.user.church
        )


class AttendanceModelForm(forms.ModelForm):
    # student = forms.ModelMultipleChoiceField(queryset=User.objects.order_by('last_name').distinct())
    
    class Meta:
        model = Attendance
        widgets = {
            'student': forms.RadioSelect(),
            'present': forms.HiddenInput()
        }
        fields = [
            "course",            
            "student",
            "attendance_date",
            "present",
        ]
        labels = {
            "student": "Person Attending",
            "course": "Class or Event",
            "attendance_date": "Date",
            "present": "Present",
        }

class SendMessageForm(forms.Form):
    subject = forms.CharField(required=True, label="Subject")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message", max_length=3000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User.objects.filter(is_active=True)
            
class RequestChurchInformation(forms.Form):
    name=forms.CharField(required=True, label="Your Name")
    phone=forms.CharField(required=True, label="Phone")
    church_name=forms.CharField(required=True, label="Church Name")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message", max_length=3000)
    email=forms.EmailField(required=True, label="Email")

class AnonPrayerRequestForm(forms.Form):
    person = forms.CharField(required=False, label="Who needs prayer? (Can be unspoken)")
    phone = forms.CharField(max_length=20, required=False)
    author = forms.CharField(max_length=100, label="Your Name")
    prayer = forms.CharField(widget=forms.Textarea, required=True, label="Prayer Request", max_length=3000)
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    class Meta:
        model = Church
        fields = [
            "prayer",
            "person",
            "church",
            "author",
            "phone",
        ]
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["church"].queryset = Church.objects.all() 

class PrayerRequestModelForm(forms.ModelForm):
    person = forms.CharField(required=False, label="Who needs prayer? (Can be unspoken)")
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    author = forms.ModelChoiceField(queryset=User.objects.order_by('last_name').values_list('last_name', flat=True).distinct())
    class Meta:
        model = PrayerRequest
        fields = [
            "prayer",
            "person",
            "church",
            "author",
        ]
        labels = {
            "prayer": "What is the situation?",
        }
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["church"].queryset = Church.objects.all()        
        self.fields["author"].queryset = User.objects.all()


class PrayerCircleForm(forms.Form):
    prayer = forms.CharField(widget=forms.Textarea, required=True, label="Prayer Request", max_length=3000)


class EditUserModelForm(forms.ModelForm):

     class Meta:
        model = User
        fields = [
            "first_name",            
            "last_name",
            "email",
            "phone_number",
            "street_address",
            "street_address_line_2",
            "city",
            "state_abbrev",
            "zip_code",
        ]
        labels = {
            "first_name": "First Name",            
            "last_name": "Last Name",
            "email": "Email",
            "phone_number": "Phone Number",
            "street_address": "Street Address - Line 1",            
            "street_address_line_2": "Street Address - Line 1",
            "city": "City",
            "state_abbrev": "Two Digit State Abbreviation",
            "zip_code": "Zip Code",
        }

class UserModelForm(forms.ModelForm):

     class Meta:
        model = User
        widgets = {
            'church': forms.RadioSelect()
        }

        fields = [
            "username",
            "password",
            "first_name",            
            "last_name",
            "email",
            "phone_number",
            "street_address",
            "street_address_line_2",
            "city",
            "state_abbrev",
            "zip_code",
            'church',
        ]
        labels = {        
            "username":"Username",
            "password":"Password",
            "first_name": "First Name",            
            "last_name": "Last Name",
            "email": "Email",
            "phone_number": "Phone Number",
            "street_address": "Street Address - Line 1",            
            "street_address_line_2": "Street Address - Line 2",
            "city": "City",
            "state_abbrev": "Two Digit State Abbreviation",
            "zip_code": "Zip Code",
        }

class CourseModelForm(forms.ModelForm):
    day = forms.CharField(required=False, label="If this is a weekly event, on what day does it occur? (optional)")
    start_date = forms.DateField(required=False, label="Starting Date of Event (optional)")
    start_time = forms.TimeField(input_formats=('%I:%M %p',...,...), required=False, label="Starting Time of Event (optional)")
    end_date = forms.DateField(required=False, label="Ending Date of Event (optional)")
    end_time = forms.TimeField(input_formats=('%I:%M %p',...,...), required=False, label="Ending Time of Event (optional)")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description of Event (optional)")
    teacher = forms.ModelChoiceField(queryset=User.objects.order_by('last_name').distinct(), required=False, label="Who teaches this class? (optional)")
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').distinct(), required=False)
    

    class Meta:
        model = Course
        fields = [
            "course_title",
            "teacher",
            "church",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "description",
            "day", 
        ]
        labels = {
            "course_title": "Name of Class or Event",
            }
    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get("instance")
    #     super(CourseModelForm, self).__init__(*args, **kwargs)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["member","course"]

        labels = {
            "member": "Who is Registering?",
            "course": "Event or Class",
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop("instance", None)
        request = kwargs.pop("request", None)
        super(RegistrationForm, self).__init__(*args, **kwargs)
 
class AccountsModelForm(forms.ModelForm):
    account_number = forms.IntegerField(required=True, label="Account Number")
    routing_number = forms.IntegerField(required=True, label="Routing Number")
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description of Account")
    name = forms.CharField(widget=forms.Textarea, required=False, label="Account Name")
    beginning_balance = forms.DecimalField(required=True, label="Beginning Balance")
    account_type = forms.ChoiceField(required=False, choices=ACCOUNTTYPE, label="Account Type")
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())

    class Meta:

        model = Accounts

        fields = [
            "account_number",
            "routing_number",
            "description",
            "name",
            "beginning_balance",
            "account_type",
            "church",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['church'].queryset = Church.objects.all()

TRANSACTION_TYPE = [
    ("One-Time","One-Time"),
    ("Monthly","Monthly"),
    ]

class DateInput(forms.DateInput):
    input_type = 'date'

class EnterContributionsForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('first_name').values_list('first_name', flat=True).distinct())
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    amount = forms.DecimalField(required=True, label="Amount of Contribution")
    send_date = forms.DateField(widget=DateInput,required=False, label="Date to Send Contribution")
    fund = forms.CharField(required=False, label="Would you like this contribution to go to a specific fund, such as building, missions or something else?  (optional)")
    transaction_type = forms.ChoiceField(required=False, choices=TRANSACTION_TYPE, label="One-Time or Monthly Contribution")
    agreement = forms.BooleanField(required=False,initial=False,)
    status = forms.BooleanField(required=False,initial=False,)

    class Meta:
        model = Contribution

        fields = [
            "user",
            "church",
            "amount",
            "send_date",
            "fund",
            "transaction_type",
            "agreement",
            "status",
        ]


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            super().__init__(*args, **kwargs)
            self.fields['church'].queryset = Church.objects.filter(id=user.church.id)
            self.fields['user'].queryset = User.objects.filter(is_active=True, church_id=user.church.id)

Gender_TYPE = [
    ("male","male"),
    ("female","female"),
    ]

US_STATES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))


COUNTRY = [
    ("US","US"),
    ]

class PaymentDetailForm(forms.ModelForm):
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    first_name = forms.CharField(required=True,label="First Name")
    last_name = forms.CharField(required=True,label="Last Name")
    id_number = forms.CharField(required=True,label="SSN",max_length=9,min_length=9, widget=forms.TextInput(attrs={'placeholder': 'Enter 9 digit number'}))
    phone = forms.CharField(required=True,label="Phone Number",max_length=10,min_length=10, widget=forms.TextInput(attrs={'placeholder': 'Enter 10 digit number'}))
    gender = forms.ChoiceField(required=True, choices=Gender_TYPE,label="Gender")
    country = forms.ChoiceField(required=True, choices=COUNTRY,label="Country")
    state = forms.ChoiceField(required=True, choices=US_STATES,label="State")
    city = forms.CharField(required=True, label="City")
    town = forms.CharField(required=False, label="Town")
    line1 = forms.CharField(required=True, label="Line1 (Street address")
    postal_code = forms.CharField(required=True, label="Postal Code")
    date_of_birth = forms.DateField(widget=DateInput, required=True, label="Date of birth")

    class Meta:
        model = Payment_Detials

        fields = [
            "church",
            "first_name",
            "last_name",
            "id_number",
            "phone",
            "gender",
            "country",
            "state",
            "city",
            "town",
            "line1",
            "postal_code",
            "date_of_birth",
        ]


    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        self.fields['church'].queryset = Church.objects.filter(id=church.id)

class BankDetailForm(forms.ModelForm):
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    account_number = forms.CharField(required=True,label="Bank Account Number")
    routing_number = forms.CharField(required=True,label="Bank Rounding Number")
    account_holder_name = forms.CharField(required=True,label="Account Holder Name")

    class Meta:
        model = Bank_Details

        fields = [
            "church",
            "account_number",
            "routing_number",
            "account_holder_name",
        ]


    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        self.fields['church'].queryset = Church.objects.filter(id=church.id)

class IdentityVerificationForm(forms.ModelForm):
    name = forms.CharField()
    church = forms.ModelChoiceField(queryset=Church.objects.order_by('name').values_list('name', flat=True).distinct())
    image = forms.ImageField()

    class Meta:
        model = Identity_Verification
        fields = [
            "name",
            "church",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        church = kwargs.pop('church', None)
        super().__init__(*args, **kwargs)
        self.fields['church'].queryset = Church.objects.filter(id=church.id)