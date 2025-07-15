from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_filter = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug")


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "condition", "created_at")
    list_filter = ("category", "condition", "created_at")
    search_fields = ("title", "description")
    fields = ("user", "title", "description", "image_url", "category", "condition")



@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ("ad_sender", "ad_receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("ad_sender__title", "ad_receiver__title", "comment")
    fields = ("ad_sender", "ad_receiver", "comment", "status")
    readonly_fields = ("created_at",)
