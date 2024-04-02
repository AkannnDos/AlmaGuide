from django.contrib.gis.db import models as geomodels
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated At'))
    
    class Meta:
        abstract = True


class BaseGeoModel(geomodels.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Updated At'))
    
    class Meta:
        abstract = True