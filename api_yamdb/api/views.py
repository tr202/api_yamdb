import re

from http import HTTPStatus

from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import filters

#from .permissions import IsOwnerOrReadOnly
from titles.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, ReviewSerializer, CommentSerializer)

#  EXTRACT_POST_ID_PATTERN = r'posts\/([0-9]+)'

'''Заглушки viewsets'''


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    ...


class ReviewViewSet(viewsets.ModelViewSet):
    ...


class CommentViewSet(viewsets.ModelViewSet):
    ...
