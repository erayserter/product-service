from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreateUserAPIView, RetrieveDestroyUserAPIView


urlpatterns = [
    path('', CreateUserAPIView.as_view(), name='user-create'),
    path('/<str:username>', RetrieveDestroyUserAPIView.as_view(), name='user-detail'),

    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
