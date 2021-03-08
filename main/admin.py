from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Identity_Verification,Members, Attendance, Minutes, Church, Course, Registration, User,Payment_Detials,Bank_Details

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone_number",
        "city",
    )
    list_filter = (
        "city",
        "state_abbrev",
    )
    search_fields = (
        "name",
        "email",
        "phone_number",
        "city",
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "attendance_date",
        "present"
    )
    # list_filter = (
    #     "student",
    #     "course",
    #     "attendance_date",
    # )
    search_fields = (
        "student",
        "course",
        "attendance_date",
    )

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "course",
    )
    # list_filter = (
    #     "member",
    #     "course",
    # )
    search_fields = (
        "member",
        "course",
    )
    raw_id_fields = ['member']

@admin.register(Members)
class MembersAdmin(admin.ModelAdmin):

    list_filter = (
        "user__email",
        "user__phone_number",
        "user__street_address",
        "user__street_address_line_2",
        "user__city",
        "user__state_abbrev",
        "user__zip_code",
    )
    search_fields = (
        "user__last_name",
        "user__first_name",
        "user__email",
        "user__phone_number",
        "user__street_address",
    )
    raw_id_fields = ['user']

class UserAdminAdvanced(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('church',"phone_number",
            "street_address",
            "street_address_line_2",
            "city",
            "state_abbrev",
            "zip_code",)}),
    )
    list_display = (
        "id",
        "username",
        "last_name",
        "first_name",
        "church",
        )
    list_filter = (
        "church",
        "groups__name",
        "city",
        "state_abbrev",
        "zip_code",
    )
    search_fields = (
        "last_name",
        "first_name",
        "church",
    )
admin.site.register(User, UserAdminAdvanced)
admin.site.register(Payment_Detials)
admin.site.register(Bank_Details)
admin.site.register(Identity_Verification)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "course_title",
        "teacher",
        )
    list_filter = (
        "course_title",
        "teacher",
    )
    search_fields = (
        "course_title",
        "teacher",
        "start_date",
        "start_time",
        "end_date",
        "end_time",
        "day",
        "description",
        )

@admin.register(Minutes)
class MinutesAdmin(admin.ModelAdmin):
    list_display = (
        "meeting_date",
        "recorder",
        "datestamp",
    )

