from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from reviews.models import AttractionReview, TourReview


@admin.register(AttractionReview)
class AttractionReviewAdmin(admin.ModelAdmin):
    list_display = ('get_attraction', 'user', 'rate', 'created_at')
    list_display_links = ('get_attraction', 'user', 'rate', 'created_at')

    def get_attraction(self, obj):
        return getattr(obj.attraction, f'name_{self.request.LANGUAGE_CODE}')
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        self.request = request
        return super().get_queryset(request).select_related(
            'attraction', 'user'
        )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest,
                              obj: Any | None = ...) -> bool:
        return False


@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('get_tour', 'user', 'rate', 'created_at')
    list_display_links = ('get_tour', 'user', 'rate', 'created_at')

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
