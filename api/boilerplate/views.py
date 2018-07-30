from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status
from .serializers import UserSerializer, GroupSerializer, MessageSerializer
from .models import Message
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Max
from .exceptions import ServiceUnavailable
import requests
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer



#Generic REST API for Messages:

class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        body = json.loads(request.body)
        userid = body["userid"]

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_message = serializer.save()

        url = "http://rasa:5005/conversations/{}/respond".format(userid)
        query = "\n".join(body["content"])
        try:
            r = requests.post(url, data=json.dumps({"query": query}))
        except:
            raise ServiceUnavailable
        highest_timestamp_db = Message.objects.all().aggregate(Max('timestamp'))['timestamp__max']
        message = Message(userid=userid,
            content=[i["text"] for i in r.json()],
            reference=question_message,
            timestamp=max(timezone.now(), highest_timestamp_db) + timedelta(seconds=120)

        )
        message.save()

        serializer = MessageSerializer(message)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)















