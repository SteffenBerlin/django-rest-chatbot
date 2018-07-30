from django.db import models
from django.urls import reverse
import json
from django.utils import timezone


class Message(models.Model):
	userid = models.CharField(max_length=255)
	content = models.TextField()
	timestamp = models.DateTimeField()
	reference = models.ForeignKey(
		'Message',
		on_delete=models.CASCADE,
		null=True
	)

	def set_content(self, content):
		self.content = json.dumps(content)

	def get_content(self):
		return json.loads(self.content)