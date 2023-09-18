from django.urls import path

from product.views import (
    RetrieveProductAPIView,
    CreateProductAPIView,
    ListProductAPIView,
    UpdateProductAPIView,
    DestroyProductAPIView
)

urlpatterns = [
    path('<str:code>', RetrieveProductAPIView.as_view()),
    path('', ListProductAPIView.as_view()),
    path('create/', CreateProductAPIView.as_view()),
    path('update/<str:code>', UpdateProductAPIView.as_view()),
    path('delete/<str:code>', DestroyProductAPIView.as_view()),
]
