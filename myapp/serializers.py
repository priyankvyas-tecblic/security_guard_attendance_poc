from rest_framework import serializers
from .models import User,AttendanceHistory,SecurityAttendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AttendanceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceHistory
        fields = "__all__"

class SecurityAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityAttendance
        fields = "__all__"
