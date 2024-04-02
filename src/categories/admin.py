from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from categories.models import Category, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'created_at')
    list_display_links = ('id', 'get_name', 'created_at')

    def get_name(self, obj):
        return getattr(obj, f'name_{self.request.LANGUAGE_CODE}')
    
    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)
    

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'get_category', 'created_at')
    list_display_links = ('id', 'get_name', 'get_category', 'created_at')

    def get_name(self, obj):
        return getattr(obj, f'name_{self.request.LANGUAGE_CODE}')
    
    get_name.shor_description = _('Name')
    
    def get_category(self, obj):
        category = obj.category
        return getattr(category, f'name_{self.request.LANGUAGE_CODE}')
    
    get_category.shor_description = _('Category')
    
    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request).select_related(
            'category'
        )
