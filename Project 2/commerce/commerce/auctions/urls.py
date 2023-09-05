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
    path("new_bid/<int:id>", views.new_bid, name="new_bid")
]
