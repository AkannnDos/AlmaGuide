from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.choices import ValueChoices
from utils.models import BaseGeoModel, BaseModel


class Attraction(BaseGeoModel):
    name_en = geomodels.CharField(max_length=255, verbose_name=_('Name EN'))
    name_ru = geomodels.CharField(max_length=255, verbose_name=_('Name RU'))
    name_kk = geomodels.CharField(max_length=255, verbose_name=_('Name KK'))
    description_en = geomodels.TextField(blank=True, null=True,
                                      verbose_name=_('Description EN'))
    description_ru = geomodels.TextField(blank=True, null=True,
                                      verbose_name=_('Description RU'))
    description_kk = geomodels.TextField(blank=True, null=True,
                                      verbose_name=_('Description KK'))
    subcategory_id = geomodels.ForeignKey('categories.Subcategory',
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Subcategory'),
                                       related_name='attractions')
    avg_rate = geomodels.DecimalField(max_digits=3, decimal_places=2,
                                   verbose_name=_('Avarage rating'))
    location = geomodels.PointField(verbose_name=_('Location'), srid=4326,
                          geography=True)

    class Meta:
        verbose_name = _('Attraction')
        verbose_name_plural = _('Attractions')
        db_table = 'attraction'


class Detail(BaseModel):
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE,
                                   verbose_name=_('Attraction'),
                                   related_name='details')
    name_en = models.CharField(max_length=255, verbose_name=_('Name EN'))
    name_ru = models.CharField(max_length=255, verbose_name=_('Name RU'))
    name_kk = models.CharField(max_length=255, verbose_name=_('Name KK'))
    value = models.CharField(max_length=255, verbose_name=_('Value'))
    value_type = models.CharField(max_length=255, choices=ValueChoices.choices,
                                  default=ValueChoices.TEXT)

    class Meta:
        verbose_name = _('Attraction detail')
        verbose_name_plural = _('Attractions details')
        db_table = 'detail'


class ChoseAttraction(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='chosen_attraction')
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE,
                                   verbose_name=_('Attraction'),
                                   related_name='users_chosen')
    
    class Meta:
        verbose_name = _('Attraction chosen')
        verbose_name_plural = _('Attractions choosen')
        db_table = 'chosen_attraction'
