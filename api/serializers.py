from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import fields
from rest_framework import serializers
from .models import Poem, Citate


class VerifyInputSerializer(serializers.Serializer):
    """
    Сериализация для входных данных GET запроса для выдачи похожести
    данных на цитаты классика
    """

    query = serializers.CharField()
    number = serializers.IntegerField(min_value=1, max_value=100, default=10)


class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Poem


class CitateSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    poem = PoemSerializer()

    def get_score(self, obj):
        return int(self.context.get('score', 0))

    class Meta:
        fields = ('line', 'lemmed_line', 'poem', 'score')
        model = Citate


class VerifyOutputSerializer(serializers.Serializer):
    """
    Сериализация для выходных данных GET запроса для выдачи похожести
    данных на цитаты классика
    """

    query = serializers.CharField()
    similar = serializers.ListField(child=CitateSerializer())
    score = serializers.IntegerField(default=0, min_value=0, max_value=100)
