from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from django.utils.translation import gettext_lazy as _

from attractions.models import (
    Attraction, Detail
)


class DetailInline(admin.TabularInline):
    model = Detail


@admin.register(Attraction)
class AttractionAdmin(geoadmin.GISModelAdmin):
    list_display = ('id', 'get_name', 'created_at')
    list_display_links = ('id', 'get_name', 'created_at')
    inlines = [DetailInline]

    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 12,
            'default_lon': 76.906639,
            'default_lat': 43.237099,
        },
    }

    def get_name(self, obj):
        return getattr(obj, f'name_{self.request.LANGUAGE_CODE}')
    
    get_name.short_description = _('Name')

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)