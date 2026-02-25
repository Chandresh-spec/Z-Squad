import os
from django.db import models
from django.conf import settings


def user_file_path(instance, filename):
    """Store files in: media/user_files/<user_id>/<filename>"""
    return os.path.join("user_files", str(instance.user.id), filename)


class UserFile(models.Model):
    """
    Represents a file uploaded by a user.
    The actual file is stored on disk under MEDIA_ROOT.
    """

    FILE_TYPE_CHOICES = [
        ("PDF", "PDF"),
        ("TXT", "TXT"),
        ("MD", "Markdown"),
        ("HTML", "HTML"),
        ("RTF", "RTF"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="files",
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_file_path)
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    size = models.PositiveBigIntegerField(default=0)  # bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "library_user_files"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.email} — {self.title}"

    def delete(self, *args, **kwargs):
        """Delete the physical file from disk when the DB record is removed."""
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)


class UserReadingData(models.Model):
    """
    Tracks all reading state for one user + one file:
    progress, PDF page, highlights, notes, bookmark flag.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reading_data",
    )
    file = models.ForeignKey(
        UserFile,
        on_delete=models.CASCADE,
        related_name="reading_data",
    )
    progress = models.FloatField(default=0.0)     # 0–100 percent
    pdf_page = models.PositiveIntegerField(default=1)
    bookmarked = models.BooleanField(default=False)
    highlights = models.JSONField(default=list)   # [{id, cls, text, ts}]
    notes = models.JSONField(default=list)        # [{text, quote, ts}]
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "library_reading_data"
        unique_together = ("user", "file")

    def __str__(self):
        return f"{self.user.email} — {self.file.title} ({self.progress:.0f}%)"
