from django.contrib import admin
from .models import Ward, Complaint, Upvote, Province, Municipality, District, ComplaintUpdate

# Register your models here.

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_np']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'province']
    list_filter = ['province']

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'district', 'total_wards']
    list_filter = ['name', 'district__province']
    search_fields = ['name']
@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['municipality', 'ward_number']
    search_fields = ['municipality__name']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'ward', 'created_at']
    list_filter = ['category', 'status']
    search_fields = ['title', 'description']

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'complaint', 'created_at']

@admin.register(ComplaintUpdate)
class ComplaintUpdateAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'old_status', 'new_status', 'updated_by', 'created_at']