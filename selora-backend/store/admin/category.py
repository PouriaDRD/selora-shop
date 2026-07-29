from django.contrib import admin

from store.models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
    ]
    prepopulated_fields = {
        "slug": ("name",),
    }
