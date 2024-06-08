from rest_framework_simplejwt.views import TokenRefreshView
import user.views as views
from django.urls import path

app_name = "user"

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
