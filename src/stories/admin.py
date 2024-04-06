from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from stories.models import Story


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('get_title', 'created_at')
    list_display_links = ('get_title', 'created_at')

    def get_title(self, obj):
        return getattr(obj, f'title_{self.request.LANGUAGE_CODE}')

    get_title.short_description = _('Title')

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        self.request = request
        return super().get_queryset(request)
