from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from attractions.models import Attraction
from tours.models import Tour
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


@receiver(post_save, sender=AttractionReview)
def handle_attraction_review(sender, instance, **kwargs):
    avg = AttractionReview.objects.filter(
        attraction_id=instance.attraction_id).aggregate(
            avg_rate=models.Avg('rate'))
    Attraction.objects.filter(id=instance.attraction_id).update(
        avg_rate=avg['avg_rate'])


@receiver(post_save, sender=TourReview)
def handle_attraction_review(sender, instance, **kwargs):
    avg = TourReview.objects.filter(
        tour_id=instance.tour_id).aggregate(
            avg_rate=models.Avg('rate'))
    Tour.objects.filter(id=instance.tour_id).update(
        avg_rate=avg['avg_rate'])
