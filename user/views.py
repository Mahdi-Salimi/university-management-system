from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView
from user.models import Assistant, Professor, Student
from user.permissions import CustomModelPermission
from user.filters import StudentFilter, ProfessorFilter
from user.serializers import StudentSerializer, ProfessorSerializer, AssistantSerializer


class LoginAPIView(TokenObtainPairView): ...


class LogoutAPIView(TokenBlacklistView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomModelViewSet(ModelViewSet):
    def get_queryset(self):
        model = self.queryset.model
        model_name = model._meta.model_name
        queryset = {"all": False, "faculty": False, "self": False}
        if self.request.method == "GET":
            if self.request.user.has_perm(f"user.view_{model_name}"):
                queryset["all"] = True
            elif self.request.user.has_perm(f"user.view_{model_name}_faculty"):
                queryset["faculty"] = True
            elif self.request.user.has_perm(f"user.view_{model_name}_self"):
                queryset["self"] = True
        elif self.request.method in ("PUT", "PATCH"):
            if self.request.user.has_perm(f"user.change_{model_name}"):
                queryset["all"] = True
            elif self.request.user.has_perm(f"user.change_{model_name}_faculty"):
                queryset["faculty"] = True
            elif self.request.user.has_perm(f"user.change_{model_name}_self"):
                queryset["self"] = True
        elif self.request.method == "DELETE":
            if self.request.user.has_perm(f"user.delete_{model_name}"):
                queryset["all"] = True
            elif self.request.user.has_perm(f"user.delete_{model_name}_faculty"):
                queryset["faculty"] = True
        if queryset["all"]:
            return model.objects.all()
        if queryset["faculty"]:
            faculty = self.request.user.get_faculty()
            if faculty:
                return model.filter_by_faculty(faculty)
        if queryset["self"]:
            return model.objects.filter(user=self.request.user)
        return model.objects.none()

    def get_object(self):
        if self.kwargs.get("pk") == "me":
            instance = self.request.user.get_role()
            model = self.queryset.model
            if isinstance(instance, model):
                self.kwargs["pk"] = instance.id
        return super().get_object()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        kwargs["partial"] = True
        if "user" in request.data:
            if "national_id" not in request.data["user"]:
                request.data["user"]["national_id"] = instance.user.national_id
        return self.update(request, *args, **kwargs)


class StudentViewSet(CustomModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter


class ProfessorViewSet(CustomModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [CustomModelPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfessorFilter


class AssistantViewSet(CustomModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [DjangoModelPermissions]
