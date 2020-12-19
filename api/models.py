from django.db import models
from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Poem(models.Model):
    name = models.CharField(
        db_index=True, max_length=200, verbose_name='Название')
    author = models.CharField(
        db_index=True, max_length=200, verbose_name='Автор')
    date_from = models.IntegerField(
        db_index=True,
        blank=True,
        null=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(
                datetime.now().year)
        ),
        verbose_name='Дата начала')
    date_to = models.IntegerField(
        db_index=True,
        blank=True,
        null=True,
        validators=(
            MinValueValidator(0),
            MaxValueValidator(
                datetime.now().year)
        ),
        verbose_name='Дата окончания')

    text = models.TextField(max_length=10000)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        title = f'author "{self.name}"'
        return title
