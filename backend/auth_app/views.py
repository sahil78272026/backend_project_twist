from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status


User = get_user_model()  # Get the correct user model


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # Get the token of the current user
    token = Token.objects.get(user=request.user)
    print("token in logout" ,token)
    token.delete()  # Invalidate the token
    return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not (username and password and email):
        return Response({'error': 'Missing fields'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )
    print("User Object Created : ",user)
    return Response({'message': 'User created successfully'})


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)


    if user:
        print("User Authenticated :", user)
        token, created = Token.objects.get_or_create(user=user)
        print('Token Created for User :', token )
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Ensure Token Authentication is used
@permission_classes([IsAuthenticated])
def dashboard(request):
    print("In Dashboad")
    return Response({'message': 'Welcome to your dashboard'})