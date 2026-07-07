from django.urls import path

from .views import ContentDetailView, ContentListView

urlpatterns = [
    path("contents/", ContentListView.as_view(), name="content-list"),
    path("contents/<int:pk>/", ContentDetailView.as_view(), name="content-detail"),
]