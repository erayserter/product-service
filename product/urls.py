from django.urls import path

from product.views import (
    RetrieveUpdateDestroyProductAPIView,
    ListCreateProductAPIView
)

urlpatterns = [
    path('/<str:code>', RetrieveUpdateDestroyProductAPIView.as_view()),
    path('', ListCreateProductAPIView.as_view()),
]
