from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ward(models.Model):
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE, null=True, blank=True)
    ward_number = models.IntegerField()
    
    def __str__(self):
        return f"{self.municipality} - Ward {self.ward_number}"
    
class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Road', 'Bato'),
        ('Water', 'Khane Pani'),
        ('Electricity', 'Bijuli'),
        ('Garbage', 'Fohor'),
        ('Other', 'Aru'), 
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('acknowledged', 'Acknowledged'),
        ('pending', 'Pending'), 
        ('in_progress', 'In Progress'), 
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    photo = models.ImageField(upload_to='complaint_photos/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)  # GPS latitude
    longitude = models.FloatField(blank=True, null=True) # GPS longitude
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.ward}"
    
class Upvote(models.Model):  # "Mero wada ma ni yahi problem xa"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'complaint')  # Ek user le ek complaint ma matra ek patak upvote garna sakos

    def __str__(self):
        return f"Upvote for {self.complaint.title} - {self.status}"
    
# Province model 
class Province(models.Model):
    name = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Municipality(models.Model):
    TYPES = [
        ('Metropolitan', 'Metropolitan City'),
        ('sub_Metropolitan', 'Sub-Metropolitan City'),
        ('municipality', 'Municipality'),
        ('rural', 'Rural Municipality'),
    ]
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_np = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPES)
    total_wards = models.IntegerField()

    def __str__(self):
        return self.name