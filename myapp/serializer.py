from rest_framework import serializers
from myapp.models import AttendanceHistory,SecurityAttendance


class AttendanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceHistory
        fields = "__all__"

class SecurityAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAttendance
        fields = "__all__"
