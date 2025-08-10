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


from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required

@login_required
def chat_home(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():  # avoid empty messages
            Message.objects.create(user=request.user, content=content)
        return redirect('chat_home')  # refresh page after sending

    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/chat_home.html', {'messages': messages})
