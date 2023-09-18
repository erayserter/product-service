from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import ListCreateUserAPIView, RetrieveDestroyUserAPIView


urlpatterns = [
    path('', ListCreateUserAPIView.as_view()),
    path('/<str:username>', RetrieveDestroyUserAPIView.as_view()),

    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
