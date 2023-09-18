from rest_framework.generics import RetrieveDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from user.serializers import UserSerializer
from user.models import User


class RetrieveDestroyUserAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class ListCreateUserAPIView(ListCreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
