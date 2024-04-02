from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class Category(BaseModel):
    name_en = models.CharField(max_length=255, verbose_name=_('Name EN'))
    name_ru = models.CharField(max_length=255, verbose_name=_('Name RU'))
    name_kk = models.CharField(max_length=255, verbose_name=_('Name KK'))
    icon = models.ImageField(upload_to='icons/',
                             validators=[
                                 FileExtensionValidator(
                                     allowed_extensions=['ico'])])
    is_popular = models.BooleanField(default=False,
                                     verbose_name=_('Is popular'),
                                     help_text=_('Only 8 categories can be '
                                                 'popular'))
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'category'


class Subcategory(BaseModel):
    name_en = models.CharField(max_length=255, verbose_name=_('Name EN'))
    name_ru = models.CharField(max_length=255, verbose_name=_('Name RU'))
    name_kk = models.CharField(max_length=255, verbose_name=_('Name KK'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name=_('Caregory'),
                                 related_name='subcategories')

    class Meta:
        verbose_name = _('Subcategory')
        verbose_name_plural = _('Subcategories')
        db_table = 'subcategory'
