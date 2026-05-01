from django.contrib import admin
from .models import Ward, Complaint, Upvote

# Register your models here.

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['municipality', 'ward_number', 'district']
    search_fields = ['municipality', 'ward_number', 'district']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'ward', 'created_at']
    list_filter = ['category', 'status']
    search_fields = ['title', 'description']

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'complaint', 'created_at']