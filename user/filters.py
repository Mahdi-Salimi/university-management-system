from django_filters import ChoiceFilter, FilterSet, CharFilter
from utils.models.choices import MilitaryServiceChoices, ProfessorRankChoices


class BaseAccountFilter(FilterSet):
    firstname = CharFilter(field_name="user__first_name", lookup_expr="icontains")
    lastname = CharFilter(field_name="user__last_name", lookup_expr="icontains")
    username = CharFilter(field_name="user__username", lookup_expr="icontains")
    national_id = CharFilter(field_name="user__national_id", lookup_expr="icontains")


class ProfessorFilter(BaseAccountFilter):
    field = CharFilter(field_name="field_of_study__name", lookup_expr="icontains")
    faculty = CharFilter(
        field_name="field_of_study__faculty_group__faculty__name",
        lookup_expr="icontains",
    )
    rank = ChoiceFilter(
        field_name="rank",
        choices=ProfessorRankChoices.choices,
    )


class StudentFilter(BaseAccountFilter):
    field = CharFilter(field_name="academic_field__field_of_study__name", lookup_expr="icontains")
    faculty = CharFilter(
        field_name="academic_field__field_of_study__faculty_group__faculty__name",
        lookup_expr="icontains",
    )
    entry_year = CharFilter(field_name="entry_semester__academic_year", lookup_expr="iexact")
    military_service = ChoiceFilter(
        field_name="military_service",
        choices=MilitaryServiceChoices.choices,
    )
