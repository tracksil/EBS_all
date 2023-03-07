from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import RegisterUserView, MyTokenObtainTokenView, UserViewList

urlpatterns = [
    path("/register", RegisterUserView.as_view(), name="token_register"),
    path("/token", MyTokenObtainTokenView.as_view(), name="token_obtain_pair"),
    path("/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("/users", UserViewList.as_view(), name="user_obtain_list"),
]
