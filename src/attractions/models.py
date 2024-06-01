from typing import Iterable
from django.contrib.gis.db import models as geomodels
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    image = models.ImageField(upload_to='attractions/', verbose_name=_('Image'))
    subcategory = geomodels.ForeignKey('categories.Subcategory',
                                       on_delete=models.CASCADE,
                                       verbose_name=_('Subcategory'),
                                       related_name='attractions')
    avg_rate = geomodels.DecimalField(max_digits=3, decimal_places=2,
                                   verbose_name=_('Avarage rating'))
    location = geomodels.PointField(verbose_name=_('Location'), srid=4326,
                          geography=True)
    is_main = geomodels.BooleanField(default=True,
                                     verbose_name=_('Show as big'),
                                     help_text=_('if checked, then another '
                                                 'checked attraction will '
                                                 'be unchecked'))
    is_on_main = geomodels.BooleanField(default=True,
                                        verbose_name=_('Show on main page'),
                                        help_text=_('there can be only 2 '
                                                    'checked in one subcategory'))
    similar_attractions = models.ManyToManyField('self', blank=True, symmetrical=True,
                                                 related_name='similars',
                                                 verbose_name=_('Similar Attractions'))

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
    value_en = models.CharField(max_length=255, verbose_name=_('Value EN'))
    value_ru = models.CharField(max_length=255, verbose_name=_('Value RU'))
    value_kk = models.CharField(max_length=255, verbose_name=_('Value KK'))
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
    route = models.ForeignKey('Route', on_delete=models.CASCADE,
                              verbose_name=_('Route'), blank=True, null=True,
                              related_name='attractions')
    
    class Meta:
        verbose_name = _('Attraction chosen')
        verbose_name_plural = _('Attractions choosen')
        db_table = 'chosen_attraction'


class Route(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='routes')
    name_en = models.CharField(max_length=255, verbose_name=_('Name EN'))
    name_ru = models.CharField(max_length=255, verbose_name=_('Name RU'))
    name_kk = models.CharField(max_length=255, verbose_name=_('Name KK'))
    
    class Meta:
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')
        db_table = 'route'


@receiver(post_save, sender=Attraction)
def after_attraction_save(sender, instance, created, **kwargs):
    if instance.is_main:
        # Если существует другой объект с полем is_main, то меняем его на False
        # Чтобы всегда был только один такой объект
        old_is_main = Attraction.objects.filter(is_main=True).exclude(
            pk=instance.pk)
        old_is_main.update(is_main=False)
    if instance.is_on_main:
        # Если существует другие объекты с полем is_on_main, то меняем старую по дате обновления на False
        # Чтобы всегда были только две таких объектов в пределах подкатегории
        another_attractions = Attraction.objects.filter(
            is_on_main=True).exclude(pk=instance.pk).order_by('updated_at')
        if another_attractions.count() >= 2:
            # если таких объектов больше или ровно 2, то старую меням на False
            to_change = another_attractions.first()
            Attraction.objects.filter(id=to_change.id).update(
                is_on_main=False)
