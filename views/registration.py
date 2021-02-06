import re

from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _
from django.views.generic import View
from project.phone import replace_phone
from users.forms import AuthenticationForm, PasswordForm, RegistrationForm

User = get_user_model()


class LogoutView(LogoutView):

    template_name = 'registration/logout.html'


class LoginView(LoginView):

    template_name = 'registration/login.html'
    form_class = AuthenticationForm


class EmailOrPhoneMixin:

    LENGTH_PASSWORD = 8

    phone_regex = _lazy_re_compile(
        r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$'
    )
    user_regex = _lazy_re_compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE
    )
    domain_regex = _lazy_re_compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE
    )

    def get(self, request):
        context = {'form': RegistrationForm()}
        return render(request, self.template_name, context)

    def put_data_to_session(self, email=None, phone=None):
        self.request.session['email'] = email
        self.request.session['phone'] = phone
        self.request.session['password'] = get_random_string(length=self.LENGTH_PASSWORD)

    def validate_phone(self, phone):
        return True if self.phone_regex.match(phone) else False

    def validate_email(self, email):
        if not email or '@' not in email:
            return False

        user_part, domain_part = email.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            return False

        if not self.domain_regex.match(domain_part):
            return False

        return True


class ResetPaswordView(EmailOrPhoneMixin, View):
    """
        Form reset password by phone or email
    """

    confirm = 'reset'
    template_name = 'registration/reset.html'

    def post(self, request):

        email_or_phone = request.POST['email_or_phone']

        form_error = _('Enter correct email or phone')

        if self.validate_email(email_or_phone):
            # Reset password by email
            if User.objects.filter(email=email_or_phone).exists():
                # send email
                self.put_data_to_session(email=email_or_phone)
                print('! ! ! password - - - - ', self.request.session['password'])
                return redirect('confirm', confirm=self.confirm)

            form_error = _('A user with that email no found.')

        if self.validate_phone(email_or_phone):
            # Reset password by phone
            if User.objects.filter(phone=email_or_phone).exists():
                # send sms
                self.put_data_to_session(phone=email_or_phone)
                print('! ! ! password - - - - ', self.request.session['password'])
                return redirect('confirm', confirm=self.confirm)

            form_error = _('A user with that phone no found.')

        context = {
            'form': RegistrationForm(request.POST),
            'form_error': form_error
        }
        return render(request, self.template_name, context)


class RegisterUserView(EmailOrPhoneMixin, View):
    """
        Form register new user by phone or email
    """

    confirm = 'register'
    template_name = 'registration/register.html'

    def post(self, request):

        email_or_phone = request.POST['email_or_phone']

        form_error = _('Enter correct email or phone')

        if self.validate_email(email_or_phone):
            # Registration by email
            if not User.objects.filter(email=email_or_phone).exists():
                # send email
                self.put_data_to_session(email=email_or_phone)
                print('! ! ! password - - - - ', self.request.session['password'])
                return redirect('confirm', confirm=self.confirm)

            form_error = _('A user with that email already exists.')

        if self.validate_phone(email_or_phone):
            # Registration by phone
            if not User.objects.filter(phone=email_or_phone).exists():
                # send sms
                self.put_data_to_session(phone=email_or_phone)
                print('! ! ! password - - - - ', self.request.session['password'])
                return redirect('confirm', confirm=self.confirm)

            form_error = _('A user with that phone already exists.')

        context = {
            'form': RegistrationForm(request.POST),
            'form_error': form_error
        }
        return render(request, self.template_name, context)


class ConfirmPaswordView(View):
    """
        Reset password or create new user by phone or email
    """

    template_name = 'registration/confirm.html'

    def get(self, request, confirm=None):
        context = {
            'form': PasswordForm(),
            'confirm': confirm
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST['password'] == request.session['password']:

            email_or_phone = request.session['email'] if request.session['email'] else request.session['phone']

            confirm = request.POST.get('confirm', None)

            # Reset password
            if confirm == 'reset':
                try:
                    user = User.objects.get(email_or_phone=email_or_phone)
                except User.DoesNotExist:
                    self.clear_session()
                    return redirect('register')

                if user:
                    user.set_password(request.session['password'])
                    user.save()

            # Create new User
            elif confirm == 'register':
                try:
                    user = User.objects.create(
                        email_or_phone=email_or_phone,
                        password=make_password(request.session['password']),
                        email=request.session['email'],
                        phone=replace_phone(request.session['phone'])
                    )
                except IntegrityError:
                    self.clear_session()
                    return redirect('register')

            if user:
                login(request, user)
                self.clear_session()
                return redirect('dashboard')

        context = {
            'form': PasswordForm(),
            'form_error': _('Wrong password')
        }
        return render(request, self.template_name, context)

    def clear_session(self):
        if 'phone' in self.request.session:
            del self.request.session['phone']
        if 'email' in self.request.session:
            del self.request.session['email']
        if 'password' in self.request.session:
            del self.request.session['password']
