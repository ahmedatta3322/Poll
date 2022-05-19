from rest_framework import generics, views
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .services import UserCreationServices, UserAuthServices
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

# Create your views here.
class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = UserCreationServices.user_process(
                request.data.get("name"), request.data.get("email")
            )
            return Response(data=response["data"], status=response["status"])
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserLoginView(views.APIView):
    def post(self, request):
        response = UserAuthServices.user_login(
            request.data.get("email"), request.data.get("password")
        )
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data=response, status=HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class RefreshTokenView(views.APIView):
    def post(self, request):

        response = UserAuthServices.refresh_token(request.data.get("access_token"))
        return Response(data=response, status=HTTP_200_OK)
