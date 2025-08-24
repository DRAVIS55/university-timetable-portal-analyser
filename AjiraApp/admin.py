from django.contrib import admin
from .models import ContactMessage,TimetableEntry
# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(TimetableEntry)
from django.contrib import admin
from .models import Advertisement

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "created_at")
    list_filter = ("active", "created_at")
    search_fields = ("title", "description")

    fieldsets = (
        ("Ad Details", {
            "fields": ("title", "description", "link", "image")
        }),
        ("Status", {
            "fields": ("active",),
        }),
    )
