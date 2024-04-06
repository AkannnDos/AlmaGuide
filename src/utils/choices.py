from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ValueChoices(TextChoices):
    TEXT = 'text', _('Simple text')
    LINK = 'link', _('Link')
    PHONE = 'phone', _('Phone number')
    