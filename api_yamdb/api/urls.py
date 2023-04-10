from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt import views as jwt_views

from .views import (CategoryViewSet, CommentViewSet,
                    GenreViewSet, TitleViewSet, ReviewViewSet,)
from users.views import SignupViewSet, YamdbUsersViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('auth/signup', SignupViewSet, 'signup')
router_v1.register('users', YamdbUsersViewSet, 'users')
router_v1.register('categories', CategoryViewSet, 'categories')
router_v1.register('genres', GenreViewSet, 'genres')
router_v1.register('titles', TitleViewSet, 'genres')
router_v1.register(r'titles\/[\d]+\/reviews', ReviewViewSet, 'reviews')
router_v1.register(r'titles\/[\d]+\/reviews\/[\d]+\/comments',
                   CommentViewSet, 'comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/',
         jwt_views.TokenObtainPairView.as_view(), name='token_obtain'),
]
