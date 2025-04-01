from django.urls import path
from .views import signup, login, dashboard, logout, UserProfileView, user_profiles, user_profile, upload_profile_image, get_user_profile

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),   # Logout API endpoint
    path('profile/', UserProfileView.as_view(), name='profile'),  # New profile endpoint
    path('profiles/', user_profiles, name='user-profiles'),  # Add this route
    path('user-profile/', user_profile, name='user-profile'),
    path('upload-image/', upload_profile_image, name='upload-profile-image'),
    path('profile_image/', get_user_profile, name='get-user-profile'),
]
