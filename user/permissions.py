from rest_framework.permissions import BasePermission


class CustomModelPermission(BasePermission):
    def has_permission(self, request, view):
        model_name = view.get_queryset().model._meta.model_name
        if request.user.is_authenticated:
            if request.method == "GET":
                if view.action == "list":
                    return (
                        request.user.has_perm(f"user.view_{model_name}")
                        | request.user.has_perm(f"user.view_{model_name}_faculty")  # fmt:skip
                    )
                elif view.action == "retrieve":
                    return (
                        request.user.has_perm(f"user.view_{model_name}")
                        | request.user.has_perm(f"user.view_{model_name}_faculty")
                        | request.user.has_perm(f"user.view_{model_name}_self")
                    )
            elif request.method in ("PUT", "PATCH"):
                return (
                    request.user.has_perm(f"user.change_{model_name}")
                    | request.user.has_perm(f"user.change_{model_name}_faculty")
                    | request.user.has_perm(f"user.change_{model_name}_self")
                )
            elif request.method == "POST":
                return request.user.has_perm(f"user.add_{model_name}")
            elif request.method == "DELETE":
                return request.user.has_perm(f"user.delete_{model_name}") | request.user.has_perm(
                    f"user.delete_{model_name}_faculty"
                )
            elif request.method == "HEAD":
                return (
                    request.user.has_perm(f"user.view_{model_name}")
                    | request.user.has_perm(f"user.view_{model_name}_faculty")
                    | request.user.has_perm("user_view_student_self")
                )
            elif request.method == "OPTIONS":
                return True
        return False
