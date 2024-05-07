from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers


class User_Serializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    
@api_view(['POST'])
def sign_up(request):
    serializer = User_Serializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        user = User(email=email, password=hashed_password)
        user.save()
        return Response({'context' : 'User Created'}, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def forgot_pass(request):
    serializer = User_Serializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        try:
            user = User.objects.get(email=email)
            hashed_password = make_password(password)
            user.password = hashed_password
            user.save()
            return Response({'context': 'Password updated successfully'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'No user with this email exists'}, status=404)
    else:
        return Response(serializer.errors, status=400)
    

@api_view(['POST'])
def sign_in(request):
    serializer = User_Serializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        msg = ''
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):  
                msg = 'Successful'
            else:
                msg = 'Wrong Password or Email'
        except User.DoesNotExist:
            msg = 'Wrong Password or Email'
        return Response({'context' : msg}, status=200)
    else:
        return Response(serializer.errors, status=400)

