from django.db import models
from django.db.models import UniqueConstraint

from users.models import YamdbUser


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='titles_genre')
    category = models.ForeignKey(
        Category, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='titles_category')
    description = models.CharField(blank=True, null=True, max_length=256)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title_genre')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name='genre_title')


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='title',)
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, related_name='rewiew',)
    score = models.IntegerField(blank=True, null=True,)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True, null=True,)

    class Meta:
        constraints = (
            UniqueConstraint(
                name='no_double_review',
                fields=['title', 'author']
            ),
        )
        ordering = ('pk',)

    def __str__(self):
        return self.text[:100]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        YamdbUser, on_delete=models.CASCADE, related_name='author',)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, blank=True, null=True,)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.text[:100]
