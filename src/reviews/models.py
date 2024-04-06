from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class AttractionReview(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                             blank=True, null=True,
                             verbose_name=_('User'),
                             related_name='reviews')
    attraction = models.ForeignKey('attractions.Attraction',
                                   on_delete=models.CASCADE,
                                   verbose_name=_('Attraction'),
                                   related_name='reviews')
    rate = models.IntegerField(verbose_name=_('Rate'))
    review = models.TextField(verbose_name=_('Review'))

    class Meta:
        verbose_name = _('Attraction review')
        verbose_name_plural = _('Attractions reviews')
        db_table = 'review'


class TourReview(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL,
                             blank=True, null=True,
                             verbose_name=_('User'),
                             related_name='tour_reviews')
    tour = models.ForeignKey('tours.Tour',
                                   on_delete=models.CASCADE,
                                   verbose_name=_('Tour'),
                                   related_name='reviews')
    rate = models.IntegerField(verbose_name=_('Rate'))
    review = models.TextField(verbose_name=_('Review'))

    class Meta:
        verbose_name = _('Tour review')
        verbose_name_plural = _('Tours reviews')
        db_table = 'tour_review'
