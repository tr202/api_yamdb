from django.db import models

from users.models import YamdbUser
from .utils import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='titles')
    description = models.CharField(blank=True, null=True, max_length=256)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title',)
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, related_name='rewiew',)
    score = models.IntegerField(blank=True, null=True,)  # Возможно лучше char
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True, null=True,)

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, related_name='author',)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True, null=True,)

    def __str__(self):
        return self.text[:100]
