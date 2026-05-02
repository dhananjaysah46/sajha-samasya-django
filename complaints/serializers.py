from rest_framework import serializers
from .models import Complaint, Ward, Municipality, District, Province, Upvote

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'name_np']

class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = District
        fields = ['id', 'name', 'name_np', 'province']

class MunicipalitySerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = Municipality
        fields = ['id', 'name', 'name_np','type', 'total_wards', 'district']

class WardSerializer(serializers.ModelSerializer):
    municipality = MunicipalitySerializer(read_only=True)

    class Meta:
        model = Ward
        fields = ['id', 'ward_number', 'municipality']

class ComplaintSerializer(serializers.ModelSerializer):
    ward = WardSerializer(read_only=True)
    ward_id = serializers.PrimaryKeyRelatedField(queryset=Ward.objects.all(), source='ward', write_only=True)
    user = serializers.StringRelatedField(read_only=True)
    upvotes_count = serializers.IntegerField(source='upvotes.count', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'title', 'description', 'category', 'category_display',
            'status', 'status_display', 'photo', 'latitude', 'longitude',
            'created_at', 'user', 'ward', 'ward_id', 'upvote_count']
        read_only_fields = ['user', 'created_at']

    def get_upvote_count(self, obj):
        return Upvote.objects.filter(complaint=obj).count()