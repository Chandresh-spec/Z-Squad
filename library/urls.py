from django.urls import path
from .views import (
    UserFileListCreateView,
    UserFileDetailView,
    UserFileServeView,
    UserReadingDataView,
)

urlpatterns = [
    # List user's files / Upload new file
    path("files/", UserFileListCreateView.as_view(), name="library-files"),

    # Delete a specific file
    path("files/<int:pk>/", UserFileDetailView.as_view(), name="library-file-detail"),

    # Serve raw file bytes (pdf.js fetches this with Authorization header)
    path("files/<int:pk>/serve/", UserFileServeView.as_view(), name="library-file-serve"),

    # Get / Update reading data (progress, highlights, notes, bookmarks)
    path("files/<int:pk>/data/", UserReadingDataView.as_view(), name="library-reading-data"),
]
