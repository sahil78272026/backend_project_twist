from django.urls import path
from .views import signup, login, dashboard, logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout, name='logout'),   # Logout API endpoint
]
