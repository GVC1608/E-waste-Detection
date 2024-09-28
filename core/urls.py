from django.urls import path
from core.views import get_form


urlpatterns = [
    path("", get_form, name="main-form")
]