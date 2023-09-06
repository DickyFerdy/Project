from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("category/<int:id>", views.category_view, name="category_view"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listed_by/<int:id>", views.listed_by, name="listed_by"),
    path("new_bid/<int:id>", views.new_bid, name="new_bid"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("transaction", views.transaction, name="transaction"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist_display, name="watchlist_display"),
    path("watchlist_add/<int:id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:id>", views.watchlist_remove, name="watchlist_remove"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("save_edit/<int:id>", views.save_edit, name="save_edit")
]
