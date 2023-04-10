from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genre

'''
class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField
    description = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    review = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

   
class Comment(models.Model):
    review = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title
'''