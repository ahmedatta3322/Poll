from .models import Poll, Choice
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class PollSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"

    def get_is_expired(self, obj):
        return obj.is_expired

