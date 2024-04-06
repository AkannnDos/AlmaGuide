from rest_framework import serializers


class StorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    uploaded_file = serializers.FileField()
    seen_count = serializers.IntegerField(
        help_text='Если больше 0, то в приложении показываем как '
                    'просмотренный')
