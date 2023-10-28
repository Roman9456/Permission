from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters
from advertisements.models import Advertisement, AdvertisementStatusChoices
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import CanDeleteAdvertisement

class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    status = filters.CharFilter(field_name='status', method='filter_status')

    def filter_status(self, queryset, name, value):
        return queryset.filter(status=value)

    class Meta:
        model = Advertisement
        fields = ['status']

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated]
    throttle_scope = 'user'

    def create(self, request, *args, **kwargs):
        data = request.data
        status = data.get('status')
        if status == AdvertisementStatusChoices.OPEN or request.method == 'POST':
            user = request.user
            open_count = Advertisement.objects.filter(creator=user, status=AdvertisementStatusChoices.OPEN).count()
            if open_count >= 10:
                return Response({"error": "You have reached the maximum number of open advertisements."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.creator != user:
            return Response({"error": "You don't have permission to update this advertisement."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.creator != user:
            return Response({"error": "You don't have permission to partially update this advertisement."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if instance.creator != user:
            return Response({"error": "You don't have permission to delete this advertisement."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)