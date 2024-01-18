from django import forms
from .models import Campsite, Profile

class AllForm(forms.Form):
    STAR_OPTIONS = [
        (1,'1 Star'),
        (2,'2 Stars'),
        (3,'3 Stars'),
        (4,'4 Stars'),
        (5,'5 Stars'),
    ]
    star_rating = forms.ChoiceField(choices=STAR_OPTIONS, required=True, widget=forms.RadioSelect)
    site_description = forms.CharField(widget=forms.Textarea, min_length=15)

    OPTIONS = [
        (1, "Yes"),
        (-1, "No"),
    ]
    allows_campfires = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    potable_water = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    outhouse = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    nearby_trees = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    trail_access = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    has_bugs = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    equipment_access = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)
    privacy_rating = forms.ChoiceField(choices=OPTIONS, required=False, widget=forms.RadioSelect)

    

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
    