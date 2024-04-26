from typing import Any
from django.contrib import admin
from django.http import HttpRequest

from exchanges.models import Exchange


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'rate', 'created_at')
    list_display_links = ('id', 'currency', 'rate', 'created_at')

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False
    