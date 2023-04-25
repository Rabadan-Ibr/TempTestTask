from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class Entity(models.Model):
    modified_by = models.ForeignKey('User', on_delete=models.CASCADE)
    value = models.IntegerField()
    properties = models.ManyToManyField('Property')


class Property(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)


# Ответ на второй и третий вопросы.
class EntitySerializer(serializers.ModelSerializer):
    locals()['data[value]'] = serializers.IntegerField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Entity
        fields = ('data[value]', 'properties')

    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_properties(self, obj):
        return {prop.key: prop.value for prop in obj.properties.all()}


class EntityModelViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Entity.objects.prefetch_related('properties')
    serializers = EntitySerializer
    permission_classes = (IsAuthenticated,)

    # Ответ на первый вопрос.
    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)
