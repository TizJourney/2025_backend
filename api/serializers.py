from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

class VerifyOutputSerializer(serializers.Serializer):
    """
    Сериализация для GET запроса для выдачи похожести
    данных на цитаты классика
    """

    query = serializers.CharField()
    score = serializers.IntegerField(default=0, min_value=0, max_value=100)
