from rest_framework import generics, permissions
from .models import ChatRoom, Message
from .serializers import MessageSerializer

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs.get('room_name')
        room = ChatRoom.objects.filter(name=room_name).first()
        if not room:
            return Message.objects.none()
        # optionally limit or order (we set model Meta ordering)
        return room.messages.all().order_by('-timestamp')  # newest first
