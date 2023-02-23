from django.urls import path, include
from accounts.views import SignUpView, LoginView


urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path('', include('django.contrib.auth.urls')),
]