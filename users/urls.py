# import django models/libraries
from django.urls import path

# import app modules
from . import views
urlpatterns = [
    path("register/", views.RegisterUserApiView.as_view(), name="register"),
    path("profile/<int:pk>", views.UserApiView.as_view(), name="logged-in-profile"),

    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('success/', views.SuccessView.as_view(), name='success'),
]


 

