from django.urls import path,include
from myapp.views import SecurityGuard, TimeSlotApiView, LoginApiView,AttendanceApi
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register("attendance",AttendanceApi , basename="attendance API")

urlpatterns = [
    path('login',LoginApiView.as_view()),
    path('security',SecurityGuard.as_view()),
    path('time_slot',TimeSlotApiView.as_view()),
    path('attendance/',AttendanceApi.as_view({"post":"create"})),
] + router.urls
