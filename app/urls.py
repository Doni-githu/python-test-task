from django.urls import path
from . import views
urlpatterns = [
    path("comic/", views.ComicViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("comic/<int:pk>/", views.ComicViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('ratings/', views.CreateRating.as_view()),
    path('comics/<int:pk>/rating/', views.GetRating.as_view())
]
