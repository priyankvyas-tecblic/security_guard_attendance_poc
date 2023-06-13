from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response

class SecurityGurad(APIView):
    def get(self,request):
        return Response({"msg":"worked"})