from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, Ward, Upvote
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.http import JsonResponse

# Create your views here.

def home(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    wards = Ward.objects.all()

    #filtering by category
    category = request.GET.get('category')
    if category:
        complaints = complaints.filter(category=category)

    #filtering by ward
    ward_id = request.GET.get('ward')
    if ward_id:
        complaints = complaints.filter(ward__id=ward_id)

    return render(request, 'home.html', {
        'complaints': complaints, 
        'wards': wards,
    })

# login view
@login_required
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
            latitude=latitude,
            longitude=longitude,
        )
        return redirect('home')

    wards = Ward.objects.all()
    return render(request, 'submit_complaint.html', {'wards': wards})

@login_required
def upvote_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    #Already upvoted?
    existing = Upvote.objects.filter(user=request.user, complaint=complaint)
    if existing.exists():
        existing.delete()  # Remove upvote
    else:
        Upvote.objects.create(user=request.user, complaint=complaint)  # Add upvote

    return redirect('home')

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
