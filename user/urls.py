from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
import user.views as views
from django.urls import path

app_name = "user"

router = DefaultRouter()
router.register(r"students", views.StudentViewSet, basename="student")
router.register(r"professors", views.ProfessorViewSet, basename="professor")
router.register(r"admin/assistants", views.AssistantViewSet, basename="admin-assistant")
router.register(r"admin/students", views.StudentViewSet, basename="admin-student")
router.register(r"admin/professors", views.ProfessorViewSet, basename="admin-professors")
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
