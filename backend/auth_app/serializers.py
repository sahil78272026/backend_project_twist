from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser
from backend.settings import MEDIA_URL

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile']

class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name', 'email','age', 'gender', 'mobile_number','profile_image']

    def get_profile_image(self, obj):
        print("In get_profile_image func")
        try:
            image_url =  f"http://127.0.0.1:8000{obj.profile_image.url}"
        except:
            image_url = None

        return image_url

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add any other profile fields you want
