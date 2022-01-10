from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_page, name="page"),
    path("search/", views.find_page, name="search"),
    path("new_page/", views.create_page, name="new_page"),
    path("edit_page/<str:title>", views.edit_page, name="edit_page"),
    path("random_page/", views.get_random_page, name="random_page"),
]
