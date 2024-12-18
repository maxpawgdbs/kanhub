__all__ = ()
from rest_framework import serializers

from apps.repositories.models import Commit, Repository, Task


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = "__all__"
        read_only_fields = ["user"]


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = "__all__"
        read_only_fields = ["user"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["user"]
