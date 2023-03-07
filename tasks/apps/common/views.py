from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.


class HealthView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response(
            {
                "live": True,
            }
        )


class ProtectedTestView(APIView):
    def get(self, request):
        return Response(
            {
                "live": True,
            }
        )
