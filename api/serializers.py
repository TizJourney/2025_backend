from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers


class VerifyInputSerializer(serializers.Serializer):
    """
    Сериализация для входных данных GET запроса для выдачи похожести
    данных на цитаты классика
    """

    query = serializers.CharField()


class VerifyOutputSerializer(serializers.Serializer):
    """
    Сериализация для выходных данных GET запроса для выдачи похожести
    данных на цитаты классика
    """

    query = serializers.CharField()
    converted_query = serializers.CharField()
    score = serializers.IntegerField(default=0, min_value=0, max_value=100)
