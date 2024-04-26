from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Exchange(BaseModel):
    currency = models.CharField(max_length=5, verbose_name=_('Currency'))
    rate = models.DecimalField(max_digits=100, decimal_places=2,
                               verbose_name=_('Rate'))
    
    class Meta:
        verbose_name = _('Exchange')
        verbose_name_plural = _('Exchanges')
        db_table = 'exchange'
        ordering = ('currency',)
