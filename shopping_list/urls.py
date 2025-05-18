from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.addItem, name="add"),
    path("complete/<int:item_id>/", views.completeItem, name="complete"),
    path("deleteitem/<int:item_id>/", views.deleteItem, name="deleteitem"),
    path("deleteall/", views.deleteAll, name="deleteall"),
    path("item/<int:item_id>/", views.item_detail, name="item_detail"),
    path("item/<int:item_id>/edit/", views.edit_item, name="edit_item"),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
