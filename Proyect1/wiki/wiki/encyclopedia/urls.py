from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.render_entry, name="entry_page"),
    path("error", views.error, name="error"),
    path("add_page", views.add_page, name="add_page"),
    path("wiki/<str:title>/edit_page", views.edit_page, name="edit_page"),
    path("save_changes", views.save_changes, name="save_changes"),
    path("random_page", views.random_page, name="random_page")
]
