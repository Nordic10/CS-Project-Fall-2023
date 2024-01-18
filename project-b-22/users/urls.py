from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name='home'),
    path("logout", views.logout_view, name='logout'),
    path('profile/',views.profile, name='profile'),
    path("<int:campsite_id>/", views.details, name='details'),
    path("<int:campsite_id>/review/", views.review, name='review'),
    path("search/", views.search_places, name='search_places'),
    path("<int:campsite_id>/<int:review_id>/delete/", views.review_delete, name='review_delete'),
    path("<int:error_number>/<int:campsite_id>/denied/", views.denied, name='denied'),
    path("createcampsite/<path:name>/<path:address>/", views.create_campsite, name="create_campsite"),
    path("approval/", views.review_approve, name="review_approve"),
    path("approve_one/<int:review_id>",views.approve_one,name="approve_one"),
    path("approve_all/", views.approve_all, name="approve_all"),
    path('upload_profile_picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("addtofav/<int:campsite_id>",views.addtofav,name="addtofav"),
    path("removefromfav/<int:campsite_id>",views.removefromfav,name="removefromfav"),
    path('google-auth-redirect/', views.auth_redirect, name='auth_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)