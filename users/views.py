# import django models/libraries
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
# import DRF models/libraries
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import render,HttpResponse
from django.conf import settings
from .serializers import UserSerializer, UserCreateSerializer
from .models import CustomUser
#from flask import Flask, request, redirect, render_template
from django.views.generic import TemplateView
from django.shortcuts import redirect

class RegisterUserApiView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @login_required
class UserApiView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializer

    def get(self, request, pk, format=None):
        user_instance = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        By using put, file has to be submitted again.
        Partial update can be done by using patch.
        """
        user_instance = get_object_or_404(CustomUser, pk=pk)
        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(instance=user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Use patch instead of update. Using patch doesn't require fields.
        Only changed values have to be passed.
        """
        user_instance = get_object_or_404(CustomUser, pk=pk)
        # pass the upload instance and the changed values to serializer
        serializer = UserSerializer(
            instance=user_instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_instance = get_object_or_404(CustomUser, pk=pk)
        try:
            user_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentView(TemplateView):
    template_name = 'users/payment.html'
    success_url = 'success'  # Specify your success URL here
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_publishable_key'] = 'pk_test_51KHRNlIKN3Fcl5ZyQ199M22PMFkGmTkdvTMTAxGvczX1xVpW9nHxFY75TRqxUiuJGgzHN8D1b2yTb04Lo4uBpGKT00SghhsrBl'
        return context
    def post(self, request, *args, **kwargs):
        
        
        token = request.POST.get('stripeToken')
        amount = 1000  # Replace with the actual amount

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='Payment for Django project'
            )

            return redirect(self.success_url)
            
        except stripe.error.CardError as e:
            # Handle the card error
            return redirect('payment')





class SuccessView(TemplateView):
    template_name = 'users/success.html'