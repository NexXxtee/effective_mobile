from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import CustomLoginForm, CustomRegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = CustomLoginForm


class CustomRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomRegisterForm
    success_url = reverse_lazy("users:login")

def custom_logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('ads:ad_list')
    return redirect('ads:ad_list')