from django.test import TestCase, Client
from .models import Campsite, Review
from .forms import AllForm
from .views import create_campsite

class CampsiteModelTest(TestCase):
    def test_campsite_rating_was_updated(self):
        campsite = Campsite(total_rating=2,num_of_ratings=2)
        campsite.total_rating = float(campsite.total_rating) + (float(5) - float(campsite.total_rating)) / float(campsite.num_of_ratings + 1)
        campsite.num_of_ratings += 1
        self.assertEquals(campsite.total_rating,3)
        self.assertEquals(campsite.num_of_ratings,3)

class WebpageRenderTest(TestCase):
    def setUp(self):
        self.client = Client()
#    def test_search(self):
#        response = self.client.get("/search/?query=sica+hollow")
#        self.assertEqual(response.status_code, 200)
#        self.assertTemplateUsed(response,"users/search.html")
    def test_logout(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)


class FormTest(TestCase):
    def test_valid(self):
        form = AllForm(data={"star_rating":1,"site_description":"test rating needs 15"})
        self.assertTrue(form.is_valid())
    def test_options(self):
        form = AllForm(data={"star_rating": 3, "site_description": "test rating needs 15", "privacy_rating": 1,"potable_water":1})
        self.assertTrue(form.is_valid())
    def test_outofrangerating(self):
        form = AllForm(data={"star_rating": 6, "site_description": "test rating needs 15"})
        self.assertFalse(form.is_valid())
    def test_outofrangeprivacy(self):
        form = AllForm(data={"star_rating": 4, "site_description": "test rating needs 15", "privacy_rating": 2})
        self.assertFalse(form.is_valid())
    def test_nodescription(self):
        form = AllForm(data={"star_rating": 4, "site_description": ""})
        self.assertFalse(form.is_valid())
    def test_norating(self):
        form = AllForm(data={"site_description": "asd;lkfhas;ldfkhsdfs"})
        self.assertFalse(form.is_valid())
