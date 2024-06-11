from functools import wraps
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import get_user_model
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView
from user.models import Assistant, Professor, Student
from user.permissions import CustomModelPermission
from user.filters import StudentFilter, ProfessorFilter
from user.tasks import send_change_pass_otp, verify_change_pass_otp
from user.serializers import (
    ChangePasswordRequestSerializer,
    ChangePasswordVerifySerializer,
    StudentSerializer,
    ProfessorSerializer,
    AssistantSerializer,
)


User = get_user_model()


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


class ChangePasswordViewSet(GenericViewSet):
    def get_serializer_class(self):
        if self.action == "request":
            return ChangePasswordRequestSerializer
        else:
            return ChangePasswordVerifySerializer

    def action_decorator(func):
        @wraps(func)
        def wrapper(self, request):
            if request.user.is_authenticated:
                user = request.user
            else:
                try:
                    username = request.data.get("username")

                    if not username:
                        return Response({"error": "Pleae enter your username!"}, status=status.HTTP_404_NOT_FOUND)
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer_class()(
                data=request.data,
            )

            if serializer.is_valid():
                if user.email:
                    return func(user=user, serializer=serializer)
                else:
                    return Response({"error": "No email associated with this user!"}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return wrapper

    @action(
        name="Change Password Request",
        detail=False,
        methods=["POST"],
        url_path="change-password-request",
        url_name="request",
    )
    @action_decorator
    def request(user, *args, **kwargs):
        send_change_pass_otp(user)
        return Response({"message": "Password change request sent successfully"}, status=status.HTTP_200_OK)

    @action(
        name="Change Password Verify",
        detail=False,
        methods=["POST"],
        url_path="change-password-action",
        url_name="verify",
    )
    @action_decorator
    def verify(user, serializer):
        sent_otp = serializer.validated_data.get("otp")
        if not verify_change_pass_otp(user, sent_otp):
            return Response({"error": "OTP expired or invalid"}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.change_password(user)
        return Response({"Password changed successfully."}, status=status.HTTP_200_OK)


DjangoModelPermissions
