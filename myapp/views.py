import os

from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from datetime import datetime, timedelta
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated

load_dotenv()

def divide_time_slots(start_time, end_time, time_difference):
    slots = []
    current_time = start_time
    while current_time < end_time:
        slots.append(current_time)
        print(current_time)
        current_time += timedelta(minutes=time_difference)
    slots.append(end_time)
    return slots


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
    def post(self,request):
        data = request.data
        data['security_guard'] = request.user
        return Response({"msg":"worked"}, status=HTTP_200_OK )