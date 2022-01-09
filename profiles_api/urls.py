from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_api import views


# for viewsets:
router = DefaultRouter()
router.register(
    "hello-viewset", views.HelloViewSet, base_name="hello-viewset"
)  # set base name when there is no queryset or when you want to override
router.register(
    "profile", views.UserProfileViewSet
)  # don't set base_name because we have queryset in view
router.register(
    "feed", views.UserProfileFeedViewSet
)

# for views
urlpatterns = [
    path("hello-view/", views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path("", include(router.urls)),
]
