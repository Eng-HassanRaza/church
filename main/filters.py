from .models import User, Members, Minutes, Course, Attendance, Church, PrayerRequest, Registration

from study.models import VerseStudyEntry

import django_filters

class MemberFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        lookup_expr="icontains", label="First Name"
    )
    last_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Last Name"
    )
    class Meta:
        model = Members
        fields = {}

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(
        lookup_expr="icontains", label="First Name"
    )
    last_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Last Name"
    )
    class Meta:
        model = User
        fields = {}

class ChurchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains", label="Name"
    )
    city = django_filters.CharFilter(
        lookup_expr="icontains", label="City"
    )
    class Meta:
        model = Church
        fields = {}

class MinutesFilter(django_filters.FilterSet):
    recorder__user__first_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Recorder's First Name"
    )
    recorder__user__last_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Recorder's Last Name"
    )
    meeting_date = django_filters.DateFilter(
    lookup_expr="icontains", label="Date"
    )
    minutes_details = django_filters.CharFilter(
    lookup_expr="icontains", label="Topic or Keywords"
    )
    class Meta:
    	model = Minutes
    	fields = {}

class AttendanceFilter(django_filters.FilterSet):
    #  course_teacher__last_name = django_filters.CharFilter(
    #     lookup_expr="icontains", label="Teacher Last Name Contains (Complete Name Not Required)"
    # )
    #  course_teacher = models.ForeignKey(Teacher, on_d
    attendance_date = django_filters.DateFilter(
        lookup_expr="icontains", label="Date"
    )
    course__course_title = django_filters.CharFilter(
        lookup_expr="icontains", label="Event or Meeting"
    )

    student__first_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Attendee First Name"
    )
    student__last_name = django_filters.CharFilter(
        lookup_expr="icontains", label="Attendee Last Name"
    )

    class Meta:
    	model = Attendance
    	fields = {}

class PrayerFilter(django_filters.FilterSet):
    person = django_filters.CharFilter(
        lookup_expr="icontains", label="For Whom"
    )
    prayer = django_filters.CharFilter(
        lookup_expr="icontains", label="Prayer Requested"
    )
    datestamp = django_filters.DateFilter(
        lookup_expr="icontains", label="Date Requested"
    )
    class Meta:
        model = PrayerRequest
        fields = {}

class CourseFilter(django_filters.FilterSet):
    course_title = django_filters.CharFilter(
        lookup_expr="icontains", label="Name of Event or Class"
    )
    class Meta:
        model = Course
        fields = {}

class RegistrationFilter(django_filters.FilterSet):

    course__course_title = django_filters.CharFilter(
        lookup_expr="icontains", label="Event"
    )

    class Meta:
        model = Registration
        fields = {}
