from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Story(BaseModel):
    title_en = models.CharField(max_length=255, verbose_name=_('Title EN'))
    title_ru = models.CharField(max_length=255, verbose_name=_('Title RU'))
    title_kk = models.CharField(max_length=255, verbose_name=_('Title KK'))
    uploaded_file = models.FileField(upload_to='stories/',
                                     verbose_name=_('Uploaded file'))

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Stories')
        db_table = 'story'


class SeenStory(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             related_name='seen_stories')
    story = models.ForeignKey(Story, on_delete=models.CASCADE,
                              verbose_name=_('Story'),
                              related_name='users_seen')

    class Meta:
        verbose_name = _('Seen story')
        verbose_name_plural = _('Seen stories')
        db_table = 'seen_story'
