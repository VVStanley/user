from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from project.phone import PhoneField


class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.CharField(
        _('email address'),
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[EmailValidator()],
        error_messages={
            'unique': _("A user with that email address already exists."),
        },
    )
    phone = PhoneField(
        _("phone"),
        unique=True,
        blank=True,
        null=True,
        error_messages={
            'unique': _("A user with that phone already exists."),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_or_phone = models.CharField(
        _('email or phone'),
        max_length=40,
        unique=True,
        help_text=_(
            'Attention!'
        ),
    )

    objects = MyUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email_or_phone'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
