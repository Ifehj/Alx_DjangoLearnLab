from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView
from django.urls import path


urlpatterns = [
    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls

urlpatterns = router.urls + [
    path('feed/', FeedView.as_view(), name='feed'),
]