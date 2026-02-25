from rest_framework import serializers

class OptimizeReadingRequestSerializer(serializers.Serializer):
    file_id = serializers.IntegerField(required=False, allow_null=True)
    text = serializers.CharField(required=False, allow_blank=True, help_text="Optional text to analyze. If not provided, it tries to fetch text from UserFile.")
    current_settings = serializers.JSONField(default=dict)

    def validate(self, data):
        if not data.get('file_id') and not data.get('text'):
            raise serializers.ValidationError("Either 'file_id' or 'text' must be provided.")
        return data


class OptimizeReadingResponseSerializer(serializers.Serializer):
    readability_score = serializers.FloatField()
    difficulty_level = serializers.CharField()
    recommended_settings = serializers.JSONField()
    actions_taken = serializers.ListField(child=serializers.CharField())
    analysis_details = serializers.JSONField(required=False)
