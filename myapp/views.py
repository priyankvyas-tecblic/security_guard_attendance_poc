import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from datetime import datetime, timedelta
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated
# from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import F, Avg
from django.contrib.auth import authenticate
from myapp.utils import get_tokens_for_user
from rest_framework import status
from django.utils.timezone import now
from .serializers import LoginSerializer, UserSerializer,AttendanceHistorySerializer,SecurityAttendanceSerializer
from .models import User,SecurityAttendance,AttendanceHistory
from django.contrib.auth.hashers import make_password

load_dotenv()

# Create your views here.
def divide_time_slots(start_time, end_time, time_difference):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time)
        print(current_time)
        current_time += timedelta(minutes=time_difference)
    slots.append(end_time)
    return slots


class LoginApiView(APIView):
    authentication_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            print("query ===>", User.objects.filter(username=username))
            user = authenticate(username=username, password=password)
            print("user = ", user)
            if user:
                user_serializer = UserSerializer(user)
                user.save()
                token = get_tokens_for_user(user)
                response = user_serializer.data
                response["token"] = token
                response = {"data": response, "status": status.HTTP_200_OK}
                return Response(response, status=status.HTTP_200_OK)
            return Response(
                {
                    "message": "Invalid Email or Password",
                    "status": status.HTTP_400_BAD_REQUEST,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotApiView(APIView):
    def get(self, request):
        start_time = datetime.strptime(os.environ.get('start_time_day'), '%H:%M:%S')
        end_time = datetime.strptime(os.environ.get('end_time_day'), '%H:%M:%S')
        time_difference = int(os.environ.get('time_difference'))
        slots = []
        time_slots = divide_time_slots(start_time, end_time, time_difference)
        for slot in time_slots:
            slots.append(slot.strftime("%H:%M:%S"))
        return Response({'slots':slots}, status=HTTP_200_OK)


class SecurityGuard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data = SecurityAttendance.objects.filter(security_guard=request.user).aggregate(
            working_hour=(
                F('check_out_time') - F('check_in_time'),
            )
        )
        print("data --->", data)
        serializer = SecurityAttendanceSerializer(data, many=True)

        return Response({"attendance":serializer.data}, status=HTTP_200_OK )

class AttendanceApi(ViewSet):
    parser_classes = (MultiPartParser, FormParser, )
    permission_classes = [IsAuthenticated]
    def create(self,request):
        user = request.user
        securityattendace = SecurityAttendance.objects.filter(security_guard = user).last()
        is_checkout = request.data.get("is_checkout", False)

        if securityattendace is None:
            request.data["check_in_time"] = now().strftime("%H:%M:%S")
            request.data["security_guard"] = user.id
            request.data["is_checkin"] = True
            serializer = SecurityAttendanceSerializer(data=request.data, context={'latitude':request.data['latitude'],
                                                      'longitude':request.data['longitude']})
            if serializer.is_valid(raise_exception=True):
                attendanceid = serializer.save()
            request.data["attendance_id"] = attendanceid.id
            serializer = AttendanceHistorySerializer(data =request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"msg":"Checked In"}, status=HTTP_200_OK )

        if securityattendace.is_checkin and securityattendace.is_checkout:
            request.data["check_in_time"] = now().strftime("%H:%M:%S")
            request.data["is_checkin"] = True
            request.data["security_guard"] = user.id
            serializer = SecurityAttendanceSerializer(data =request.data, context={'latitude':request.data['latitude'],
                                                      'longitude':request.data['longitude']})
            if serializer.is_valid(raise_exception=True):
                attendanceid = serializer.save()
            request.data["attendance_id"] = attendanceid.id
            serializer = AttendanceHistorySerializer(data =request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"msg":"Checked In"}, status=HTTP_200_OK )

        elif securityattendace.is_checkin == True and securityattendace.is_checkout == False and not is_checkout:
            request.data["attendance_id"] = securityattendace.id
            serializer = AttendanceHistorySerializer(data =request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"msg":"Checked In"}, status=HTTP_200_OK )
                
        elif securityattendace.is_checkin == True and securityattendace.is_checkout == False and is_checkout:
            request.data["check_out_time"] = now().strftime("%H:%M:%S")
            serializer = SecurityAttendanceSerializer(securityattendace, data=request.data, partial=True,
                                                      context={'latitude':request.data['latitude'],
                                                      'longitude':request.data['longitude']})
            if serializer.is_valid(raise_exception=True):
                attendanceid = serializer.save()
            request.data["attendance_id"] = attendanceid.id
            
            serializer = AttendanceHistorySerializer(data =request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({"msg":"Checked Out"}, status=HTTP_200_OK )
        return Response({"msg":"not worked"}, status=HTTP_200_OK )            
