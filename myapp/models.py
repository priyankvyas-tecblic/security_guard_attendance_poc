from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SecurityAttendance(models.Model):
    security_guard = models.ForeignKey(User, related_name='security_guard', on_delete=models.CASCADE)
    check_in_time = models.TimeField(null=True,blank=True)
    check_out_time = models.TimeField(null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_checkin = models.BooleanField(default=True)
    is_checkout = models.BooleanField(default=False)


class AttendanceHistory(models.Model):
    attendance_id = models.ForeignKey(SecurityAttendance, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/')
    upload_time = models.TimeField(auto_now_add=True)
    upload_date = models.DateField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)