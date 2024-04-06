from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tour', 'user', 'paid', 'created_at')
    list_display_links = ('id', 'get_tour', 'user', 'paid', 'created_at')

    def get_tour(self, obj):
        return getattr(obj.tour, f'title_{self.request.LANGUAGE_CODE}')
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        self.request = request
        return super().get_queryset(request).select_related(
            'tour', 'user'
        )
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False
