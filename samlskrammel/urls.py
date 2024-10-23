from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("leaderboard", views.leaderboard, name="login"),
    path("log-på", views.login, name="login"),
    path("log-ud", views.logout, name="logout"),
    path("opret-bruger", views.opret_bruger, name="opret_bruger"),
    path("opret-oplæg", views.opret_oplaeg, name="opret_oplaeg"),
    path("tilføj-ven", views.tilfoej_ven, name="tilfoej_ven"),
]
