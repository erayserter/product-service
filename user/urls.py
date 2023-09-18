from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import UserDetailAPIView, UserCreateAPIView


urlpatterns = [
    path('<int:pk>/', UserDetailAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
