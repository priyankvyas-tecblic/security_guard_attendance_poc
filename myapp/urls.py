from django.urls import path,include
from myapp.views import SecurityGuard, TimeSlotApiView
urlpatterns = [
    path('security',SecurityGuard.as_view()),
    path('time_slot',TimeSlotApiView.as_view())
]
