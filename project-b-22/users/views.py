from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import requests
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import urllib.parse
from allauth.socialaccount import providers
from allauth.socialaccount.templatetags.socialaccount import get_providers

from .models import Campsite, Review, Favorites

from .forms import AllForm
from .forms import ProfilePicForm

def campsite_rating_refresh(campsite):
    count = 0
    sum = 0
    for r in campsite.reviews.all():
        if (r.approved):
            sum += float(r.rating)
            count += 1
    if count != 0:
        campsite.total_rating = sum/count
    else:
        campsite.total_rating = 0
    campsite.save()
    return count

def home(request):
    info = {
        "campsite_list": Campsite.objects.all(),
    }
    if request.user.is_authenticated:
        info["is_admin"] = request.user.groups.filter(name='Admin').exists()
    return render(request, "users/home.html", info)
    
def profile(request):
    if not(request.user.is_authenticated):
        return HttpResponseRedirect("/1/0/denied/") 
    if request.user.groups.filter(name='Admin').exists():
        new_review.approved = True
    info = {
        "email": request.user.email,
    }
    return render(request, "users/profile.html", info)

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfilePicForm(instance=request.user.profile)
    return render(request, 'users/upload_profile_picture.html', {'form': form})

def details(request, campsite_id):
    campsite = get_object_or_404(Campsite, pk=campsite_id)
    reviews = []
    for r in campsite.reviews.all():
        if r.approved:
            reviews.append(r)
    info = {
        "campsite": campsite,
        "reviews": reviews,
        "star_range": range(1, 6),  
    }
    if request.user.is_authenticated:
        info["is_admin"] = request.user.groups.filter(name='Admin').exists()
    return render(request, "users/details.html", info)



def review(request, campsite_id):
    if not(request.user.is_authenticated):
        return HttpResponseRedirect("/1/0/denied/") 
    campsite = get_object_or_404(Campsite, pk=campsite_id)
    for r in campsite.reviews.all():
        if request.user.email == r.user_email:
            return HttpResponseRedirect("/0/" + str(campsite_id) + "/denied/")
    if request.method == "POST":
        form = AllForm(request.POST)
        if form.is_valid():
            new_review = Review(campsite = campsite, user_email = request.user.email, site_description = form.cleaned_data['site_description'], rating = form.cleaned_data['star_rating'])
            sifter = [
                form.cleaned_data['allows_campfires'],
                form.cleaned_data['potable_water'],
                form.cleaned_data['outhouse'],
                form.cleaned_data['nearby_trees'],
                form.cleaned_data['trail_access'],
                form.cleaned_data['has_bugs'],
                form.cleaned_data['equipment_access'],
                form.cleaned_data['privacy_rating'],
            ]
            size = len(sifter)
            for i in range(0, size):
                if sifter[i] != "-1" and sifter[i] != "1":
                    sifter[i] = 0
            new_review.allows_campfires = sifter[0]
            new_review.potable_water = sifter[1]
            new_review.outhouse = sifter[2]
            new_review.nearby_trees = sifter[3]
            new_review.trail_access = sifter[4]
            new_review.has_bugs = sifter[5]
            new_review.equipment_access = sifter[6]
            new_review.privacy_rating = sifter[7]

            if request.user.groups.filter(name='Admin').exists():
                new_review.approved = True
            new_review.save()
            campsite.num_of_ratings = campsite_rating_refresh(campsite)
            campsite.save()

            return HttpResponseRedirect("/" + str(campsite_id) + "/")
    
    else:
        form = AllForm()
    info = {
        "campsite": campsite,
        "form": form,
    }
    return render(request, "users/review.html", info)

def review_delete(request, campsite_id, review_id):
    if not(request.user.groups.filter(name='Admin').exists()):
        return HttpResponseRedirect("/1/0/denied/") 
    review = get_object_or_404(Review, pk=review_id)
    campsite = get_object_or_404(Campsite, pk=campsite_id)
    was_approved = review.approved
    info = {
        "campsite": campsite,
        "reviews": campsite.reviews.all(),
    }
    if request.method == 'POST':
        review.delete()
        campsite.num_of_ratings = campsite_rating_refresh(campsite)
        campsite.save()
        if was_approved:
            return HttpResponseRedirect("/" + str(campsite_id) + "/")
        else:
            return HttpResponseRedirect("/approval/")
    
    return render(request, 'users/delete.html', info)

def review_approve(request):
    if not(request.user.groups.filter(name='Admin').exists()):
        return HttpResponseRedirect("/1/0/denied/") 
    reviews = []
    for r in Review.objects.all():
        if not(r.approved):
            reviews.append(r)
    empty = False
    if len(reviews) == 0:
        empty = True
    info = {
        "empty": empty,
        "reviews": reviews,
    }
    return render(request, "users/approve.html", info)

def approve_all(request):
    if not(request.user.groups.filter(name='Admin').exists()):
        return HttpResponseRedirect("/1/0/denied/") 
    for r in Review.objects.all():
        if not(r.approved):
            r.approved = True
            r.save()
    for c in Campsite.objects.all():
        c.num_of_ratings = campsite_rating_refresh(c)
        c.save()
    return HttpResponseRedirect("/")

def approve_one(request,review_id):
    if not(request.user.groups.filter(name='Admin').exists()):
        return HttpResponseRedirect("/1/0/denied/") 
    for r in Review.objects.all():
        if r.id == review_id:
            r.approved = True
            r.save()
    for c in Campsite.objects.all():
        c.num_of_ratings = campsite_rating_refresh(c)
        c.save()
    return review_approve(request)

def denied(request, error_number, campsite_id):
    info = {
        "error_number": error_number,
    }
    if error_number == 0:
        info["campsite"] = get_object_or_404(Campsite, pk=campsite_id)
    return render(request, "users/denied.html", info)

def logout_view(request):
    logout(request)
    return redirect("/")

def search_places(request):
    query = request.GET.get('query', '')
    results = []
    
    if query:
        api_key = 'AIzaSyAVwOx-8ymMZ8vm37DPUMSufX6zU58fdc4'
        endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': query,
            'type': 'campground',  
            'key': api_key
        }
        response = requests.get(endpoint_url, params=params).json()
        results = response.get('results', [])
    
    return render(request, 'users/search.html', {'results': results})



def create_campsite(request, name, address):
    for c in Campsite.objects.all():
        if c.site_name == name:
            return HttpResponseRedirect("/" + str(c.pk) + "/")
    api_key = "AIzaSyAVwOx-8ymMZ8vm37DPUMSufX6zU58fdc4"
    endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json"
    address_formatted = urllib.parse.quote(address,safe='')
    params = {
        'address': address,
        'key': api_key
    }
    response = requests.get(endpoint_url,params=params).json()
    results = response.get("results", [])
    lat_long_pair = results[0]["geometry"]["location"]
    lat = lat_long_pair["lat"]
    long = lat_long_pair["lng"]
    new_campsite = Campsite(site_name=name, site_address=address, total_rating=0, lat = lat, long = long)
    new_campsite.save()
    return HttpResponseRedirect("/" + str(new_campsite.pk) + "/")

@login_required
def profile(request):
    favorites = []
    for f in Favorites.objects.all():
        if f.user.id == request.user.id:
            favorites.append(f)
    info = {
        "favorites": favorites,
        "email": request.user.email,
    }
    return render(request, 'users/profile.html', info)

def addtofav(request,campsite_id):
    if not(request.user.is_authenticated):
        return HttpResponseRedirect("/google-auth-redirect/")
    campsite = get_object_or_404(Campsite, pk=campsite_id)
    exists = False
    for f in Favorites.objects.all():
        if f.user.id == request.user.id and f.campsite == campsite:
            exists = True
    if not exists:
        new_fav = Favorites(user=request.user,campsite=campsite)
        new_fav.save()
    return details(request,campsite_id)

def removefromfav(request,campsite_id):
    if not(request.user.is_authenticated):
        return HttpResponseRedirect("/google-auth-redirect/")
    campsite = get_object_or_404(Campsite, pk=campsite_id)
    for f in Favorites.objects.all():
        if f.user.id == request.user.id and f.campsite == campsite:
            f.delete()
    return details(request,campsite_id)

def auth_redirect(request):
    provider = providers.registry.get_class('google')
    authentication_url = provider.get_login_url(self=provider, request=request, next="/")
    return redirect(authentication_url)