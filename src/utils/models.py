from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language


class ModelDisplayMixin:

    def __str__(self):
        language_code = get_language()
        if hasattr(self, f'name_{language_code}'):
            return getattr(self, f'name_{language_code}')
        if hasattr(self, f'title_{language_code}'):
            return getattr(self, f'title_{language_code}')
        return super().__str__()


class BaseModel(ModelDisplayMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated At'))
    
    class Meta:
        abstract = True


class BaseGeoModel(ModelDisplayMixin, geomodels.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated At'))
    
    class Meta:
        abstract = True