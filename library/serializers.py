import os
from rest_framework import serializers
from .models import UserFile, UserReadingData


class UserReadingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadingData
        fields = [
            "id", "progress", "pdf_page",
            "bookmarked", "highlights", "notes", "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class UserFileSerializer(serializers.ModelSerializer):
    """
    Serializer for listing/uploading user files.
    Includes nested reading data if it exists.
    """

    reading_data = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = UserFile
        fields = [
            "id", "title", "file_type", "size",
            "uploaded_at", "file_url", "reading_data",
        ]
        read_only_fields = ["id", "uploaded_at", "file_url", "reading_data"]

    def get_reading_data(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        try:
            rd = UserReadingData.objects.get(user=request.user, file=obj)
            return UserReadingDataSerializer(rd).data
        except UserReadingData.DoesNotExist:
            return None

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request and obj.file:
            return request.build_absolute_uri(f"/api/library/files/{obj.id}/serve/")
        return None


class UserFileUploadSerializer(serializers.ModelSerializer):
    """
    Handles multipart file upload.
    Derives title from filename if not provided.
    """

    file = serializers.FileField()
    title = serializers.CharField(required=False, max_length=255)

    ALLOWED_EXTENSIONS = {"pdf", "txt", "md", "html", "rtf"}

    class Meta:
        model = UserFile
        fields = ["title", "file"]

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lstrip(".").lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError(
                f"Unsupported file type: .{ext}. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        return value

    def validate(self, attrs):
        # Auto-derive title from filename if not provided
        if not attrs.get("title"):
            name = attrs["file"].name
            attrs["title"] = (
                os.path.splitext(name)[0]
                .replace("-", " ")
                .replace("_", " ")
                .title()
            )
        return attrs

    def create(self, validated_data):
        file = validated_data["file"]
        ext = os.path.splitext(file.name)[1].lstrip(".").upper()
        return UserFile.objects.create(
            user=self.context["request"].user,
            title=validated_data["title"],
            file=file,
            file_type=ext if ext else "TXT",
            size=file.size,
        )
