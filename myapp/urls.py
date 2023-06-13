from django.urls import path,include
from myapp.views import SecurityGurad
urlpatterns = [

    path('security',SecurityGurad.as_view())
]
