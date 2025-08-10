# netbox_lcm/api/views.py
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from netbox.api.viewsets import NetBoxModelViewSet  # for permissions integration
from django_filters.rest_framework import DjangoFilterBackend
from netbox_lcm.models.external import ExternalAssessment, ExternalAssessmentType
from netbox_lcm.api.serializers import ExternalAssessmentSerializer, ExternalAssessmentTypeSerializer
from netbox_lcm.filtersets import ExternalAssessmentFilter

class ExternalAssessmentTypeViewSet(ReadOnlyModelViewSet):
    queryset = ExternalAssessmentType.objects.all()
    serializer_class = ExternalAssessmentTypeSerializer
    filter_backends = (DjangoFilterBackend,)

class ExternalAssessmentViewSet(ModelViewSet):
    """
    Create via API; updates are allowed but generally not needed.
    You may set http_method_names = ['get','post','delete'] to make rows immutable after write.
    """
    queryset = ExternalAssessment.objects.all()
    serializer_class = ExternalAssessmentSerializer
    filterset_class = ExternalAssessmentFilter
    filter_backends = (DjangoFilterBackend,)
    ordering = ("-observed_at", "-id")
