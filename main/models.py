from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

STATE_CHOICES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))


class User(AbstractUser):
    church = models.ForeignKey("Church", on_delete=models.CASCADE, null=True, blank=True, related_name="user_church")
    street_address = models.CharField(max_length=150, null=True, blank=True)
    street_address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_abbrev = models.CharField(choices=STATE_CHOICES, max_length=2, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table='auth_user_church'

    def __str__(self):
        """String for representing the Model object."""
        return "%s %s %s " % (self.first_name, self.last_name,self.phone_number)

    def get_full_short(self):
        full_short = self.first_name[:1] + ". " + self.last_name
        if len(full_short) < 3:
            return "Unknown"
        return full_short.title()

    def get_church_name_short(self):
        if self.church:
            return self.church.name.title()
        return "Unknown Church"

    def get_edit_url(self):
        return f"/user/{self.id}/update"

    def get_delete_url(self):
        return f"/user/{self.id}/delete"


class Church(models.Model):
    name = models.CharField(max_length=50, null=False)
    street_address = models.CharField(max_length=150, null=False)
    street_address_line_2 = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=False)
    state_abbrev = models.CharField(max_length=30, null=False)
    zip_code = models.CharField(max_length=11, null=False)
    phone_number = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=200, null=False)    
    stripe_id = models.CharField(max_length=250, null=False,blank=True)
    payment_verified = models.BooleanField(default=False)
    is_bank_verified = models.BooleanField(default=False)
    class Meta:
        unique_together = ('name', 'phone_number')

    def get_absolute_url(self):
        return f"/church/{self.id}"

    def get_edit_url(self):
        return f"/church/{self.id}/update"

    def get_delete_url(self):
        return f"/church/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s %s %s %s %s " % (self.name, self.street_address,
            self.city, self.state_abbrev, self.zip_code)

class Members(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    datestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Members"

    def get_absolute_url(self):
        return f"/members/{self.id}"

    def get_edit_url(self):
        return f"/members/{self.id}/update"

    def get_delete_url(self):
        return f"/members/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s" % (self.user.church)

class Course(models.Model):
    church = models.ForeignKey(Church, on_delete=models.CASCADE,related_name="course_church", null=True)
    course_title = models.CharField(max_length=250, null=False)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE,related_name="course_teacher", null=True)
    start_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_date = models.DateField(null=True)
    end_time = models.TimeField(null=True)
    day = models.CharField(max_length=250, null=True)
    description = models.CharField(max_length=2500, null=True)


    class Meta:
        unique_together = ('course_title', 'teacher')

    def get_absolute_url(self):
        return f"/events/{self.id}"

    def get_edit_url(self):
        return f"/events/{self.id}/update"

    def get_delete_url(self):
        return f"/events/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s %s " % (self.course_title, self.teacher,
            )

class Minutes(models.Model):
    meeting_date = models.DateField()
    minutes_details = models.CharField(max_length=20000, null=False)
    recorder = models.ForeignKey(User, on_delete=models.CASCADE,related_name="minutes_recorder",)
    datestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('meeting_date', 'recorder')

    def get_absolute_url(self):
        return f"/minutes/{self.id}"

    def get_edit_url(self):
        return f"/minutes/{self.id}/update"

    def get_delete_url(self):
        return f"/minutes/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s %s %s %s " % (self.meeting_date, self.minutes_details, self.recorder, self.datestamp)

class BibleVerse(models.Model):
    verse_words = models.CharField(max_length=20000, null=False)
    book = models.CharField(max_length=200, null=False)
    chapter = models.IntegerField(null=False)
    verse_number = models.IntegerField(null=False)

    class Meta:
        unique_together = ('verse_words', 'book', 'chapter', 'verse_number')

    def __str__(self):
        return "%s %s %s %s" % (self.verse_words, self.book, self.chapter, self.verse_number)

class PrayerRequest(models.Model):
    person = models.CharField(max_length=200, null=True)
    prayer = models.CharField(max_length=20000, null=False)
    datestamp = models.DateTimeField(auto_now=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE,related_name="prayer_church",)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="prayer_author", null=True)

    class Meta:
        ordering = ['-datestamp']
        unique_together = ('person','prayer',)

    def __str__(self):
        return "%s %s" % (
            self.person,
            self.prayer,            
            self.datestamp,
            self.church,
        )

    def get_edit_url(self):
        return f"/prayer/{self.id}/update"

    def get_delete_url(self):
        return f"/prayer/{self.id}/delete"

class Registration(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_registration")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="event_registration"
    )

    class Meta:
        unique_together = ("course", "member")

    def __str__(self):
        return "%s %s %s" % (self.member.first_name, self.member.last_name, self.course.course_title)

    def get_delete_url(self):
        return f"/registration/{self.id}/delete"

    def get_edit_url(self):
        return f"/registration/{self.id}/update"

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_attendance",)
    course =  models.ForeignKey(Course, on_delete=models.CASCADE,related_name="course_attendance",)
    attendance_date = models.DateField()
    present = models.BooleanField()

    class Meta:
        ordering = ["-attendance_date"]
        unique_together = ('attendance_date','student', 'course')
        
    def __str__(self):
        return "%s %s %s %s" % (
            self.attendance_date,
            self.student,
            self.course,
            self.present,
        )

    def record_attendance_url(self):
        return f"/record-attendance"

    def edit_attendance_url(self):
        return f"/attendance/{self.id}/edit-attendance"

    def get_delete_url(self):
        return f"/attendance/{self.id}/delete"



ACCOUNTTYPE = [
    ("Checking", "Checking"), 
    ("Savings", "Savings"),
    ("Accounts Receivable", "Accounts Receivable"),
    ("Other", "Other"),
    ]


class Accounts(models.Model):
    account_number = models.BigIntegerField()
    routing_number = models.BigIntegerField()    
    description = models.CharField(max_length=1000, null=False)
    name =  models.CharField(max_length=200, null=False)
    beginning_balance = models.DecimalField(max_digits=10, decimal_places=2)
    account_type = models.CharField(choices = ACCOUNTTYPE, max_length=50, null=False)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE,related_name="accounts_church", null=True)
    

    def get_absolute_url(self):
        return f"/accounts/{self.id}"

    def get_edit_url(self):
        return f"/accounts/{self.id}/update"

    def get_delete_url(self):
        return f"/accounts/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

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

class FixedAssets(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=False)
    purchase_date = models.DateField()
    disposal_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)
    sale_proceeds = models.DecimalField(max_digits=10, decimal_places=2)
    asset_type = models.CharField(choices = ACCOUNTTYPE, max_length=50, null=False)
    
      
    def get_absolute_url(self):
        return f"/fixed/{self.id}"

    def get_edit_url(self):
        return f"/fixed/{self.id}/update"

    def get_delete_url(self):
        return f"/fixed/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

CURRENTLIABILITYTYPE = [
    ("Credit Card", "Credit Card"), 
    ("Accounts Payable", "Accounts Payable"),
    ("Other", "Other"),
    ]

OPENORCLOSED = [
    ("Open", "Open"), 
    ("Closed", "Closed"),
    ]

class CurrentLiabilities(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=False)
    due_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    liability_type = models.CharField(choices = CURRENTLIABILITYTYPE, max_length=50, null=False)
    status = models.CharField(choices = OPENORCLOSED, max_length=50, null=False)
    
      
    def get_absolute_url(self):
        return f"/current-liability/{self.id}"

    def get_edit_url(self):
        return f"/current-liability/{self.id}/update"

    def get_delete_url(self):
        return f"/current-liability/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

LONGTERMTYPE = [
    ("Loan", "Loan"), 
    ("Other", "Other"),
    ]

class LongTermLiabilities(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=False)
    due_date = models.DateField()
    open_date = models.DateField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    liability_type = models.CharField(choices = LONGTERMTYPE, max_length=50, null=False)
    status = models.CharField(choices = OPENORCLOSED, max_length=50, null=False)
    
      
    def get_absolute_url(self):
        return f"/longterm-liability/{self.id}"

    def get_edit_url(self):
        return f"/longterm-liability/{self.id}/update"

    def get_delete_url(self):
        return f"/longterm-liability/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

INCOMETYPE = [
    ("Contribution","Contribution"),
    ("Grant","Grant"),
    ("Other","Other"),
    ]

class Income(models.Model):
    income_type = models.CharField(choices = INCOMETYPE, max_length=50, null=False)
    description = models.CharField(max_length=2000, null=False)
    name = models.CharField(max_length=250, null=False) 

    def get_absolute_url(self):
        return f"/income/{self.id}"

    def get_edit_url(self):
        return f"/income/{self.id}/update"

    def get_delete_url(self):
        return f"/income/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

EXPENSETYPE = [
    ("Salary","Salary"),
    ("Rent","Rent"),
    ("Bank Fee","Bank Fee"),
    ("Building Fee","Building Fee"),
    ("Office Supplies","Office Supplies"),
    ("Other","Other"),
    ]

class Expense(models.Model):
    expense_type = models.CharField(choices = EXPENSETYPE, max_length=50, null=False)
    description = models.CharField(max_length=2000, null=False)
    name = models.CharField(max_length=250, null=False) 

    def get_absolute_url(self):
        return f"/income/{self.id}"

    def get_edit_url(self):
        return f"/income/{self.id}/update"

    def get_delete_url(self):
        return f"/income/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

class Vendor(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    street_address = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_abbrev = models.CharField(choices=STATE_CHOICES, max_length=2, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True)

class Customer(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    street_address = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state_abbrev = models.CharField(choices=STATE_CHOICES, max_length=2, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True)

class Transactions(models.Model):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE,related_name="account_transaction",)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_transaction =  models.ForeignKey(Income, on_delete=models.CASCADE,related_name="income_transaction",)
    expense_transaction = models.ForeignKey(Expense, on_delete=models.CASCADE,related_name="expense_transaction",)
    description = models.CharField(max_length=1000, null=False)
    description = models.CharField(max_length=1000, null=True)

    def get_absolute_url(self):
        return f"/transactions/{self.id}"

    def get_edit_url(self):
        return f"/transactions/{self.id}/update"

    def get_delete_url(self):
        return f"/transactions/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

class AccountsPayable(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,related_name="vendor_accountspayable",)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=250, null=False) 
    due_date = models.DateField()
    memo = models.CharField(max_length=2000, null=False)
    remaining_balance =  models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return f"/accounts-payable/{self.id}"

    def get_edit_url(self):
        return f"/accounts-payable/{self.id}/update"

    def get_delete_url(self):
        return f"/accounts-payable/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)

class AccountsReceivable(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="customer_accountspayable",)
    amount =  models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=250, null=False) 
    due_date = models.DateField()
    memo = models.CharField(max_length=2000, null=False)
    remaining_balance =  models.DecimalField(max_digits=10, decimal_places=2)
    invoice_date = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return f"/accounts-receivable/{self.id}"

    def get_edit_url(self):
        return f"/accounts-receivable/{self.id}/update"

    def get_delete_url(self):
        return f"/accounts-receivable/{self.id}/delete"

    def __str__(self):
        """String for representing the Model object."""
        return "%s " % (self.id)



TRANSACTION_TYPE = [
    ("One-Time","One-Time"),
    ("Monthly","Monthly"),
    ]

class Contribution(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name="contribution_user")
    chruch = models.ForeignKey(Church,on_delete=models.CASCADE,null=True, blank=True, related_name="contribution_church")
    amount = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    send_date = models.DateField()
    fund = models.CharField(max_length=250,null=True,blank=True)
    transaction_type = models.CharField(choices = TRANSACTION_TYPE, max_length=50, null=False)
    agreement = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

Gender_TYPE = [
    ("male","male"),
    ("female","female"),
    ]

US_STATES = (('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
COUNTRY = [
    ("US","US"),
    ]
class Payment_Detials(models.Model):
    chruch = models.ForeignKey(Church, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="church_payment_details")
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=False, blank=False)
    id_number = models.CharField(max_length=250, null=False, blank=False)
    phone = models.CharField(max_length=250, null=False, blank=False)
    gender = models.CharField(choices = Gender_TYPE, max_length=50, null=False)
    country = models.CharField(choices = COUNTRY, max_length=50, null=False)
    state = models.CharField(choices=US_STATES, max_length=50, null=False)
    city = models.CharField(max_length=250, null=False, blank=False)
    town = models.CharField(max_length=250, null=True, blank=True)
    line1 = models.CharField(max_length=250, null=False, blank=False)
    postal_code = models.CharField(max_length=250, null=False, blank=False)
    date_of_birth = models.DateField()

    class Meta:
        verbose_name_plural = "Payment_Detials"

    def get_absolute_url(self):
        return f"/payment_details/{self.id}"

    def __str__(self):
        """String for representing the Model object."""
        return "%s" % (self.first_name)

class Bank_Details(models.Model):
    chruch = models.ForeignKey(Church, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="church_bank_details")
    account_number = models.CharField(max_length=250, null=False, blank=False)
    routing_number = models.CharField(max_length=250, null=False, blank=False)
    account_holder_name = models.CharField(max_length=250, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Bank_Details"

    def get_absolute_url(self):
        return f"/bank_details/{self.id}"

    def __str__(self):
        """String for representing the Model object."""
        return "%s" % (self.account_holder_name)

