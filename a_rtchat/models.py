from django.db import models
from django.contrib.auth.models import User
import shortuuid
import os
from PIL import Image

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name
    
    meeting_id = models.CharField(max_length=255, blank=True, null=True)
    
    def get_meeting_id(self):
        if not self.meeting_id:
            self.meeting_id = f"mentorconnect-{self.group_name}"
            self.save()
        return self.meeting_id
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        elif self.file:
            return f'{self.author.username} : {self.filename}'
    
    class Meta:
        ordering = ['-created']

    @property    
    def is_image(self):
        try:
            image = Image.open(self.file) 
            image.verify()
            return True 
        except:
            return False
        
def clean(self):
    if not self.body and not self.file:
        raise ValidationError("Message must have either text or a file.")
    if self.file:
        # Validate file size (e.g., max 10MB)
        if self.file.size > 10 * 1024 * 1024:
            raise ValidationError("File size cannot exceed 10MB.")