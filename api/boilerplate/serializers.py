from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Message
from django.utils import timezone


#Serializers for Users and Groups:

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


#Serializer for Message:

class MessageSerializer(serializers.ModelSerializer):
	content = serializers.ListField(
		child = serializers.CharField(), min_length = 1
	)

	def validate_timestamp(self, value):
		if value > timezone.now():
			raise serializers.ValidationError("Timestamp is not in the past")
		return value


	class Meta:
		model = Message
		fields = ('userid', 'content', 'timestamp')