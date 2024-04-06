from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Order(BaseModel):
    tour = models.ForeignKey('tours.Tour', on_delete=models.PROTECT,
                             verbose_name=_('Tour'),
                             related_name='orders')
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                             blank=True, null=True,
                             verbose_name=_('User'),
                             related_name='orders')
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        db_table = 'order'
