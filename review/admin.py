from django.contrib import admin
from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "rating", "title", "company_name", "reviewer")
    readonly_fields = ("ip_address", )
    raw_id_fields = ("reviewer", )
    date_hierarchy = "created_at"
