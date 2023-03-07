from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import UserSerializer, UserSerializerLogIn, UsersSerializerList


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        # Get password from validated data
        password = validated_data.pop("password")

        # Create user
        user = User.objects.create(
            **validated_data,
            username=validated_data['email'],
            is_superuser=True,
            is_staff=True,
        )

        # Set password
        user.set_password(password)
        user.save()

        return Response(UserSerializer(user).data)


class MyTokenObtainTokenView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializerLogIn

    @serialize_decorator(UserSerializer)
    def post(self, request):

        user = authenticate(username=request.data.get('email'), password=request.data.get('password'))
        refresh = RefreshToken.for_user(user=user)

        data = {
            'refresh': str(refresh),
            'access_token': str(refresh.access_token),
        }

        return Response(data)


class UserViewList(GenericAPIView):
    serializer_class = UsersSerializerList

    @serialize_decorator(UsersSerializerList)
    def get(self, request):
        users = User.objects.all()
        users_serializer = UsersSerializerList(users, many=True)
        data = users_serializer.data

        return Response(data)
