from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        _('Email'),
        unique=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    full_name = models.CharField(_('Full name'), max_length=150, blank=True)
    phone_number = models.CharField(_('Phone number'), max_length=20,
                                    blank=True)
    photo = models.ImageField(_('Photo'), upload_to='photos/', blank=True,
                              null=True)
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'user'
        

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    def __str__(self) -> str:
        return self.email
