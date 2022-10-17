from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('delete-item/<int:id>/', views.deleteItem, name='delete-item'),
    # path('', views.image_upload, name='image_upload'),

    # #access the laptop camera
    # path('video_feed', views.video_feed, name='video_feed'),

    # #access the phone camera
    # path('webcam_feed', views.webcam_feed, name='webcam_feed'),
]