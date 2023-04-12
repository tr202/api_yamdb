import re
import operator
from functools import reduce
from http import HTTPStatus
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Prefetch, Q
from django.db import models
from rest_framework import request

from rest_framework import status
from rest_framework import viewsets
from rest_framework.compat import distinct
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .permissions import IsOwnerOrReadOnly, IsAdminModeratorOwnerOrReadOnly, IsAdminRole
from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from .permissions import IsAdminRoleOrStaff
from .serializers import (CategorySerializer, CreateUpdateTitleSerializer, GenreSerializer,
                          TitleSerializer, TitleDetailSerializer,
                          ReviewSerializer, CommentSerializer)

EXTRACT_TITLE_ID_PATTERN = r'titles\/([0-9]+)'
EXTRACT_TITLE_ID_AND_REVIEW_ID = r'titles\/([0-9]+)\/reviews\/([0-9]+)'
METHOD_NOT_ALLOWED = 'Method not allowed'
PAGE_SIZE = 50
PAGE_SIZE_QUERY_PARAM = 'page_size'
MAX_PAGE_SIZE = 500
FILTER_PARAMS = {'category': 'category__slug',
                 'name': 'name', 'genre': 'genre__slug', 'year': 'year'}


class StandardResultsSetPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE


class BaseCategoryGenreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminRoleOrStaff,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(METHOD_NOT_ALLOWED, status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(METHOD_NOT_ALLOWED, status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewSet(BaseCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(BaseCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TileFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_kwargs = {}
        for param in request.GET:
            print(param)
            search_kwargs[FILTER_PARAMS.get(param)] = request.GET.get(param)
        return Title.objects.filter(**search_kwargs)


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminRole,)
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (TileFilter,)
    #search_fields = ('name','genre','category','year')

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = TitleDetailSerializer
        return super(TitleViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateUpdateTitleSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            genres = Genre.objects.filter(slug__in=serializer.validated_data)
            self.perform_create(serializer, genres)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers)
        except IntegrityError:
            return Response('Already exists', HTTPStatus.BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CreateUpdateTitleSerializer
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer, genres):
        title = serializer.save()
        for genre in genres:
            GenreTitle.objects.bulk_create(genre=genre, title=title)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_title_id(self):
        pattern = EXTRACT_TITLE_ID_PATTERN
        return re.findall(pattern, self.request.path)[0]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.get_title_id())

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            title = Title.objects.get(pk=self.get_title_id())
            self.perform_create(serializer, title)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Does not exists', status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer, title):
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_ids(self):
        pattern = EXTRACT_TITLE_ID_AND_REVIEW_ID
        ids = re.findall(pattern, self.request.path)
        self.title_id = ids[0][0]
        self.review_id = ids[0][1]
        return True

    def get_queryset(self):
        self.get_ids()
        print(self.title_id, ' ', self.review_id)
        return Comment.objects.filter(review_id=self.review_id)
    
    def create(self, request, *args, **kwargs):
        self.get_ids()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            review = Review.objects.get(pk=self.review_id)
            self.perform_create(serializer, review)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Does not exists', status.HTTP_404_NOT_FOUND)
    def perform_create(self, serializer, review):
        serializer.save(author=self.request.user, review=review)
