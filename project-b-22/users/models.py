from django.contrib.auth.models import Group, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

camper_group, created = Group.objects.get_or_create(name='Camper')
admin_group, created = Group.objects.get_or_create(name='Admin')

class Campsite(models.Model):
    site_name = models.CharField(max_length=100)
    site_address = models.CharField(max_length=100, default="placeholder Dr.")
    total_rating = models.DecimalField(max_digits=2, decimal_places=1, default=None)
    num_of_ratings = models.IntegerField(default=0)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    
    
    def __str__(self):

        return self.site_name
    
class Review(models.Model):

    approved = models.BooleanField(default=False)

    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, related_name='reviews')
    user_email = models.CharField(max_length=100)

    site_description = models.CharField(max_length=10000)
    rating = models.IntegerField()

    allows_campfires = models.IntegerField(default=0)
    potable_water = models.IntegerField(default=0)
    outhouse = models.IntegerField(default=0)
    nearby_trees = models.IntegerField(default=0)
    trail_access = models.IntegerField(default=0)
    has_bugs = models.IntegerField(default=0)
    equipment_access = models.IntegerField(default=0)
    privacy_rating = models.IntegerField(default=0)


    def __str__(self):
        return self.campsite.site_name + " - " + self.user_email


DEFAULT_PROFILE_IMAGE_PATH = 'static/admin/images/defaultPFP.png'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='defaultPFP.png')
    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Favorites(models.Model):
    user = models.ForeignKey(User,related_name="favorites",on_delete=models.CASCADE)
    campsite = models.ForeignKey(Campsite,related_name="favorites",on_delete=models.CASCADE,default=None)
