from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from django.utils.translation import gettext_lazy as _

from attractions.forms import AttractionForm
from attractions.models import (
    Attraction, Detail
)


class DetailInline(admin.TabularInline):
    model = Detail


@admin.register(Attraction)
class AttractionAdmin(geoadmin.GISModelAdmin):
    list_display = ('id', 'get_name', 'is_main', 'avg_rate', 'created_at', 'is_on_main')
    list_display_links = ('id', 'get_name', 'is_main', 'avg_rate', 'created_at', 'is_on_main')
    list_filter = ('is_main', 'is_on_main')
    inlines = [DetailInline]
    filter_horizontal = ('similar_attractions',)

    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 12,
            'default_lon': 76.906639,
            'default_lat': 43.237099,
        },
    }

    form = AttractionForm

    def get_name(self, obj):
        return getattr(obj, f'name_{self.request.LANGUAGE_CODE}')
    
    get_name.short_description = _('Name')

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)