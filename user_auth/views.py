from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm, ForgotPassword
from django.contrib import messages


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user_auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'user_auth/register.html'


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("password_reset_done")
    template_name = 'user_auth/custom_password_reset_form.html'
    email_template_name = 'user_auth/custom_password_reset_email.html'

    form_class = ForgotPassword


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user_auth/custom_password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("password_reset_complete")
    template_name = "user_auth/custom_password_reset_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user_auth/custom_password_reset_complete.html"

