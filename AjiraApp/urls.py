
from django.contrib import admin
from django.urls import path
from AjiraApp import views

from django.urls import path
from . import views


from django.urls import path
from . import views





urlpatterns = [
    path('admin/', admin.site.urls),
     path("", views.home, name="home"),
    path("about-us/", views.about_us, name="about_us"),
    path("personal-profile/", views.personal_profile, name="personal_profile"),
    path("education/", views.education, name="education"),
    path("skills/", views.skills, name="skills"),
    path("experience/", views.experience, name="experience"),
    path("projects/", views.projects, name="projects"),
    path("references/", views.references, name="references"),
    path("contact/", views.contact, name="contact"),
    path('admin-messages/', views.admin_messages, name="admin_messages"),
     path("admin/messages/clear/", views.clear_messages, name="clear_messages"),
]
