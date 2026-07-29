from django.contrib import admin

from store.models import AttributeModel, AttributeValueModel


@admin.register(AttributeModel)
class AttributeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(AttributeValueModel)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = [
        "attribute",
        "value",
    ]
    list_filter = [
        "attribute",
    ]
