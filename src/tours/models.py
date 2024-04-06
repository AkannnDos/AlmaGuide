from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Tour(BaseModel):
    title_en = models.CharField(max_length=255, verbose_name=_('Title EN'))
    title_ru = models.CharField(max_length=255, verbose_name=_('Title RU'))
    title_kk = models.CharField(max_length=255, verbose_name=_('Title KK'))
    description_en = models.TextField(verbose_name=_('Description EN'))
    description_ru = models.TextField(verbose_name=_('Description RU'))
    description_kk = models.TextField(verbose_name=_('Description KK'))
    image = models.ImageField(upload_to='tours/', verbose_name=_('Image'))
    price = models.IntegerField(verbose_name=_('Price'))
    duration = models.IntegerField(verbose_name=_('Duration'))
    avg_rate = models.FloatField(default=5.0, verbose_name=_('Avarage rate'))
    way_to_travel = models.CharField(max_length=255,
                                     verbose_name=_('Way to travel'))

    class Meta:
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')
        db_table = 'tour'
