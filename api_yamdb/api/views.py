import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Prefetch

from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.response import Response

from .permissions import (IsAdminModeratorOwnerOrReadOnly,
                          IsAdminRole,
                          IsAdminRoleOrModerator)
from reviews.models import Category, Genre, GenreTitle, Title, Review, Comment
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          CreateUpdateTitleSerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleDetailSerializer,
                          ReviewSerializer)

EXTRACT_TITLE_ID_PATTERN = r'titles\/([0-9]+)'
EXTRACT_TITLE_ID_AND_REVIEW_ID = r'titles\/([0-9]+)\/reviews\/([0-9]+)'
METHOD_NOT_ALLOWED = 'Method not allowed'
PAGE_SIZE = 50
PAGE_SIZE_QUERY_PARAM = 'page_size'
MAX_PAGE_SIZE = 500
FILTER_PARAMS = {'category': 'category__slug',
                 'name': 'name',
                 'genre': 'genre__slug',
                 'year': 'year'}


class StandardResultsSetPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE


class BasePermissionViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.method in set(SAFE_METHODS):
            return (AllowAny(),)
        return super().get_permissions()


class BaseCategoryGenreViewSet(BasePermissionViewSet):
    permission_classes = (IsAdminRole,)
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
            search_kwargs[FILTER_PARAMS.get(param)] = request.GET.get(param)
        return (
            Title.objects.filter(**search_kwargs)
            .select_related('category')
            .prefetch_related('genre')
        )


class TitleViewSet(BasePermissionViewSet):
    permission_classes = (IsAdminRoleOrModerator,)
    queryset = (Title.objects.prefetch_related(
        Prefetch('titles_genre',
                 queryset=Genre.objects.only('id', 'name', 'slug')
                 )).select_related('titles_category')
                )
    serializer_class = TitleSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (TileFilter,)

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
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        self.serializer_class = CreateUpdateTitleSerializer
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer, genres):
        title = serializer.save()
        map(lambda _: GenreTitle.objects.get_or_create(title=title), genres)


class ReviewViewSet(BasePermissionViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_title_id(self):
        pattern = EXTRACT_TITLE_ID_PATTERN
        return re.findall(pattern, self.request.path)[0]

    def get_queryset(self):
        return Review.objects.filter(
            title=self.get_title_id()).select_related('author')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            title = Title.objects.get(pk=self.get_title_id())
            self.perform_create(serializer, title)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Does not exists', status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer, title):
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(BasePermissionViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_ids(self):
        pattern = EXTRACT_TITLE_ID_AND_REVIEW_ID
        ids = re.findall(pattern, self.request.path)
        self.review_id = ids[0][1]
        return True

    def get_queryset(self):
        self.get_ids()

        return (Comment.objects.filter(
                review_id=self.review_id)
                .select_related('author')
                )

    def create(self, request, *args, **kwargs):
        self.get_ids()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            review = Review.objects.get(pk=self.review_id)
            self.perform_create(serializer, review)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except IntegrityError:
            return Response('Already exists', status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('Does not exists', status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer, review):
        serializer.save(author=self.request.user, review=review)
