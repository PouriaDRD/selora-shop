from django.urls import path


from .views import CategoryListAPIView, CategoryDetailAPIView

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view(), name="category-list"),
    path("categories-detail/", CategoryDetailAPIView.as_view(), name="category-detail"),
]
