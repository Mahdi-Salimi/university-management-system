from rest_framework.routers import DefaultRouter

from .views import FacultyViewSet, FacultyGroupViewSet, FieldOfStudyViewSet, AcademicFieldViewSet

router = DefaultRouter()
router.register(r"faculties", FacultyViewSet)
router.register(r"faculty-groups", FacultyGroupViewSet)
router.register(r"fields-of-study", FieldOfStudyViewSet)
router.register(r"academic-fields", AcademicFieldViewSet)

app_name = "faculty"

urlpatterns = router.urls
