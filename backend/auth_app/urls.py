from django.urls import path
from .views import signup, login, dashboard, logout, UserProfileView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),   # Logout API endpoint
    path('profile/', UserProfileView.as_view(), name='profile'),  # New profile endpoint
]
