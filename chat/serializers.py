from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'room', 'username', 'content', 'timestamp']

    def get_username(self, obj):
        return obj.user.username if obj.user else None
