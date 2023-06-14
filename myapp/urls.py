from django.urls import path,include
from myapp.views import SecurityGuard, TimeSlotApiView, LoginApiView

urlpatterns = [
    path('login',LoginApiView.as_view()),
    path('security',SecurityGuard.as_view()),
    path('time_slot',TimeSlotApiView.as_view())
]
