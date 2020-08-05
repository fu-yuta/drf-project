from django.urls import path
from api import views

urlpatterns = [
    path('api/', views.DynamoListRequest.as_view()),
    path('api/<pk>/', views.DynamoDetailRequest.as_view())
]
