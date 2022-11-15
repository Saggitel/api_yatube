from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers

from .views import PostViewSet, GroupViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)

urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/', include(router.urls)),
]
