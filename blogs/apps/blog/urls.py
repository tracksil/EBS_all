from django.urls import path

from apps.blog.views import CategoryViewSet, BlogListView, BlogItemView, BlogCreateView, CommentCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(
    r"categories",
    CategoryViewSet,
    basename="category",
)

urlpatterns = router.urls

urlpatterns += [
    path("blog", BlogListView.as_view(), name="blog_list"),
    path("blog/<int:pk>", BlogItemView.as_view(), name="blog_item"),
    path("blog/create", BlogCreateView.as_view(), name="blog_create"),
    path("comment/create", CommentCreateView.as_view(), name="comment_create")
]
