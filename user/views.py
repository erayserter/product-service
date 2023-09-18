from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from shopping.permissions import IsPersonalAccountOrReadOnly

from user.serializers import UserSerializer
from user.models import User


class RetrieveDestroyUserAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsPersonalAccountOrReadOnly, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class CreateUserAPIView(CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
