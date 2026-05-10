from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, Municipality, Ward, Upvote, Province, District, Municipality, ComplaintUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from .serializers import ComplaintSerializer, WardSerializer, MunicipalitySerializer, DistrictSerializer, ProvinceSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator

from django.http import JsonResponse

# Create your views here.

def home(request):
    complaints_list = Complaint.objects.select_related('user','ward', 'ward__municipality', 'ward__municipality__district').order_by('-created_at')
    wards = Ward.objects.all()

    #filtering by category
    category = request.GET.get('category')
    district = request.GET.get('district')
    search = request.GET.get('search')

    if category:
        complaints_list = complaints_list.filter(category=category)
    if district:
        complaints_list = complaints_list.filter(ward__municipality__district_id=district)
    if search:
        complaints_list = complaints_list.filter(
            title__icontains=search
        ) | complaints_list.filter(
            description__icontains=search
        )

    # pagination - 10 per page
    paginator = Paginator(complaints_list, 10)
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)

    districts = District.objects.select_related('province').order_by('name')

    return render(request, 'home.html', {
        'complaints': complaints, 
        'search': search or '',
        'districts': districts,
    })

# login view
@login_required
def profile(request):
    user_complaints = Complaint.objects.filter(
        user=request.user
    ).select_related(
        'ward', 'ward__municipality'
    ).order_by('-created_at')

    user_upvotes = Upvote.objects.filter(
        user=request.user
    ).select_related(
        'complaint'
    ).order_by('-created_at')

    return render(request, 'profile.html', {
        'user_complaints': user_complaints,
        'user_upvotes': user_upvotes,
        'complaint_count': user_complaints.count(),
        'upvote_count': user_upvotes.count(),
    })

def submit_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        ward_id = request.POST.get('ward')
        photo = request.FILES.get('photo')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        ward = get_object_or_404(Ward, id=ward_id)

        Complaint.objects.create(
            title=title,
            description=description,
            category=category,
            ward=ward,
            user=request.user,
            photo=photo,
            latitude=latitude or None,
            longitude=longitude or None,
        )
        return redirect('home')

    provinces = Province.objects.all()
    return render(request, 'submit_complaint.html', {'provinces': provinces})
@login_required
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    # Sirf owner le edit garna milxa
    if complaint.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        complaint.title = request.POST.get('title')
        complaint.description = request.POST.get('description')
        complaint.category = request.POST.get('category')
        if request.FILES.get('photo'):
            complaint.photo = request.FILES.get('photo')
        complaint.save()
        return redirect('complaint_detail', complaint_id=complaint.id)

    return render(request, 'edit_complaint.html', {'complaint': complaint})


@login_required
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    # Sirf owner le delete garna milxa
    if complaint.user != request.user:
        return redirect('home')

    if request.method == 'POST':
        complaint.delete()
        return redirect('home')

    return render(request, 'delete_complaint.html', {'complaint': complaint})

@login_required
def upvote_complaint(request, complaint_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    #Already upvoted?
    existing = Upvote.objects.filter(user=request.user, complaint=complaint)
    
    if existing.exists():
        existing.delete()  # Remove upvote
        voted = False
    else:
        Upvote.objects.create(user=request.user, complaint=complaint)  # Add upvote
        voted = True
    upvote_count = Upvote.objects.filter(complaint=complaint).count()
    return JsonResponse({
        'voted': voted, 
        'upvote_count': upvote_count
        })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken!'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        return redirect('home')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials!'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# API endpoint for mapdata
def complaints_map_data(request):
    complaints = Complaint.objects.exclude(
        latitude=None
    ).exclude(longitude=None)
    
    data = []
    for c in complaints:
        data.append({
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'category': c.get_category_display(),
            'status': c.get_status_display(),
            'ward': str(c.ward),
            'user': c.user.username,
            'upvotes': Upvote.objects.filter(complaint=c).count(),
            'lat': c.latitude,
            'lng': c.longitude,
        })
    
    return JsonResponse({'complaints': data})

def map_view(request):
    return render(request, 'map.html')

# Complaint detail view
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    upvotes = Upvote.objects.filter(complaint=complaint).count()
    user_upvoted = False
    if request.user.is_authenticated:
        user_upvoted = Upvote.objects.filter(user=request.user, complaint=complaint).exists()

    return render(request, 'complaint_detail.html', {
        'complaint': complaint,
        'upvotes': upvotes,
        'user_upvoted': user_upvoted,
    })

def get_districts(request):
    province_id = request.GET.get('province_id')
    districts = District.objects.filter(province_id=province_id).values('id', 'name', 'name_np')
    return JsonResponse({'districts': list(districts)})

def get_municipalities(request):
    district_id = request.GET.get('district_id')
    municipalities = Municipality.objects.filter(district_id=district_id).values('id', 'name', 'name_np', 'type')
    return JsonResponse({'municipalities': list(municipalities)})

def get_wards(request):
    municipality_id = request.GET.get('municipality_id')
    wards = Ward.objects.filter(municipality_id=municipality_id).values('id', 'ward_number').order_by('ward_number')
    return JsonResponse({'wards': list(wards)})

def dashboard(request):
    # Total complaint stats
    total_complaints = Complaint.objects.count()
    open_complaints = Complaint.objects.filter(status='open').count()
    resolved_complaints = Complaint.objects.filter(status='resolved').count()
    total_upvotes = Upvote.objects.count()

    # Complaints by category
    category_stats = Complaint.objects.values('category').annotate(count=Count('id')).order_by('-count')

    # Complaints by district
    district_stats = Complaint.objects.values('ward__municipality__district__name').annotate(count=Count('id')).order_by('-count')[:10]  # Top 10 districts

    #Most upvoted complaints
    top_complaints = Complaint.objects.annotate(upvote_count=Count('upvotes')).order_by('-upvote_count')[:5]

    # Recent complaints
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]

    return render(request, 'dashboard.html', {
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'resolved_complaints': resolved_complaints,
        'total_upvotes': total_upvotes,
        'category_stats': category_stats,
        'district_stats': district_stats,
        'top_complaints': top_complaints,
        'recent_complaints': recent_complaints,
    })

# complaints - list + create
class ComplaintListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Complaint.objects.all().order_by('-created_at')

        # Filtering by category
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        district = self.request.GET.get('district')
        ward_id = self.request.GET.get('ward_id')

        if category:
            queryset = queryset.filter(category=category)
        
        if status:
            queryset = queryset.filter(status=status)

        if district:
            queryset = queryset.filter(ward__municipality__district__name__icontains=district)

        if ward_id:
            queryset = queryset.filter(ward_id=ward_id)

        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# complaint detail - retrieve, update, delete
class ComplaintDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# upvote API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upvote_api(request, pk):
    complaint = Complaint.objects.get(pk=pk)
    existing = Upvote.objects.filter(user=request.user, complaint=complaint)

    if existing.exists():
        existing.delete()  # Remove upvote
        return Response({'status': 'removed', 'upvotes': Upvote.objects.filter(complaint=complaint).count()})
    else:
        Upvote.objects.create(user=request.user, complaint=complaint)  # Add upvote
        return Response({'status': 'added', 'upvotes': Upvote.objects.filter(complaint=complaint).count()})
    
# Province list API
class ProvinceListAPI(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

# District list API
class DistrictListAPI(generics.ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        province_id = self.request.query_params.get('province_id')
        if province_id:
            return District.objects.filter(province_id=province_id)
        return District.objects.all()
    
# Municipality list API
class MunicipalityListAPI(generics.ListAPIView):
    serializer_class = MunicipalitySerializer

    def get_queryset(self):
        district_id = self.request.query_params.get('district_id')
        if district_id:
            return Municipality.objects.filter(district_id=district_id)
        return Municipality.objects.all()
    
# Ward list API
class WardListAPI(generics.ListAPIView):
    serializer_class = WardSerializer

    def get_queryset(self):
        municipality_id = self.request.query_params.get('municipality_id')
        if municipality_id:
            return Ward.objects.filter(municipality_id=municipality_id)
        return Ward.objects.all()
# Stats API
@api_view(['GET'])
def stats_api(request):
    category_stats = list(Complaint.objects.values('category').annotate(count=Count('id')))
    district_stats = list(Complaint.objects.values('ward__municipality__district__name').annotate(count=Count('id')).order_by('-count')[:10])

    return Response({
        'total_complaints': Complaint.objects.count(),
        'open': Complaint.objects.filter(status='open').count(),
        'acknowledged': Complaint.objects.filter(status='acknowledged').count(),
        'resolved': Complaint.objects.filter(status='resolved').count(),
        'total_upvotes': Upvote.objects.count(),
        'by_category': category_stats,
        'top_districts': district_stats,
    })