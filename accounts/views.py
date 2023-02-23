from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View
from django.contrib.auth import get_user_model, authenticate, login
from accounts.forms import SignUpForm, LoginForm
from django.template.response import TemplateResponse


class LoginView(View):
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return TemplateResponse(request, 'registration/login.html')

    def post(self, request):
        self.context = {}
        login_form = LoginForm(request.POST)

        user = authenticate(username=request.POST.get('username'), password=request.POST.get("password"))
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            self.context['wrong_credentials'] = True
        if not login_form.is_valid():
            self.context['login_form'] = login_form
        return TemplateResponse(request, 'registration/login.html', self.context)


class SignUpView(View):
    context = {}

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))

        self.context['sign_up_form'] = SignUpForm
        return TemplateResponse(request, 'registration/signup.html', self.context)

    def post(self, request):
        sign_up_form = SignUpForm(request.POST)
        if not sign_up_form.is_valid():
            self.context['sign_up_form'] = sign_up_form
        if sign_up_form.is_valid():
            sign_up_form.save()
            return HttpResponseRedirect(reverse("login"))
        return TemplateResponse(request, 'registration/signup.html', self.context)
