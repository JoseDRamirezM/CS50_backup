from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:item_id>/<int:user_id>/<str:message>", views.render_item, name="render_item"),
    path("listing/<int:item_id>", views.render_item_not_auth, name="render_item_not_auth"),
    path("listing/<int:item_id>/add_watchlist/<str:user_id>", views.add_watchlist, name="add_watchlist"),
    path("listing/<int:item_id>/remove_watchlist/<str:user_id>", views.remove_watchlist, name="remove_watchlist"),
    path("listing/<int:item_id>/place_bid/<str:user_id>", views.place_bid, name="place_bid"),
    path("listing/<int:item_id>/close_auction/<str:user_id>", views.close_auction, name="close_auction"),
    path("listing/<int:item_id>/add_comment/<str:user_id>)", views.add_comment, name="add_comment"),
    path("watchlist/<str:user_id>", views.render_watchlist, name="render_watchlist"),
    path("categories", views.show_categories, name="show_categories"),
    path("categories/sort_by_category/<str:category>", views.sort_by_category, name="sort_by_category")
]
