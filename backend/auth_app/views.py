# import from django
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password

#import from drf
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import generics, permissions

#local imports
from .models import CustomUser
from .serializers import UserProfileSerializer, ProfileSerializer

User = get_user_model()  # Get the correct user model


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Fetch the logged-in user's profile"""
    user = request.user
    print("user :", user)
    serializer = UserProfileSerializer(user)  # ✅ Use the serializer to return user data
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_image(request):
    """Upload a profile image for the logged-in user"""
    user = request.user # ✅ This is the User Profile object (instance of CustomUser)

    if 'profile_image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    image = request.FILES['profile_image']

    # Save image to user profile
    user.profile_image = image
    user.save()

    return Response({
        "message": "Profile image uploaded successfully",
        "profile_image": user.profile_image.url
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Log the user out by deleting the token"""
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "Logged out successfully"}, status=200)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=400)

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





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profiles(request):
    """Get all profiles except the logged-in user"""
    User = get_user_model()
    profiles = User.objects.exclude(id=request.user.id)
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get and update the current user's profile"""
    if request.method == 'GET':
        serializer = ProfileSerializer(request.user)
        print("In user profile GET method block")
        print("serializer :", serializer.data)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_profiles(request):
    """Search for users based on age and location"""
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    location = request.GET.get('location')

    users = CustomUser.objects.all()

    if min_age:
        users = users.filter(age__gte=min_age)  # Age greater than or equal to min_age
    if max_age:
        users = users.filter(age__lte=max_age)  # Age less than or equal to max_age
    if location:
        users = users.filter(location__icontains=location)  # Case-insensitive location match

    serializer = UserProfileSerializer(users, many=True)
    return Response(serializer.data)
