from django.contrib import admin
from myapp.models import *
# Register your models here.

@admin.register(SecurityAttendance)
class SecurityAttendanceAdmin(admin.ModelAdmin):
    list_display = ['security_guard', 'check_in_time', 'check_out_time', 'created_at']


@admin.register(AttendanceHistory)
class AttendanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['attendance_id', 'latitude', 'longitude', 'upload_time', 'upload_date']

