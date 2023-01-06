from rest_framework import serializers
from .models import Follower
from django.db import IntegrityError


class FollowerSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_name = serializers.ReadOnlyField(source='followed.username')

    class Meta:
        model = Follower
        fields = ['owner', 'followed_name']

    def create(self, validated_data):
        try:
            follower = Follower.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Follower already exists")
        return follower
