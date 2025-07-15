from django.urls import path
from .views import CustomLoginView, CustomRegisterView, custom_logout_view

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', custom_logout_view, name='logout'),
]