from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from .validators import validate_icon_image_size, validate_image_file_extension

def server_icon_upload_path(instance, filename):
    return f'server/{instance.id}/server_icon/{filename}'

def server_banner_upload_path(instance, filename):
    return f'server/{instance.id}/server_banner/{filename}'

def category_icon_upload_path(instance, filename):
    return f'category/{instance.id}/category_icon/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icon_upload_path', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id:
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Category")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon' or field.name == 'banner':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name

class Server(models.Model):
    name = models.CharField(max_length=100)
    owner =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='server_owner')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='server_category')
    description = models.CharField(max_length=250, null=True, blank=True)
    member = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='server_member')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channel_owner')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='channel_server')
    topic = models.CharField(max_length=250, null=True, blank=True)
    banner = models.ImageField(
        upload_to='channel_banner_upload_path',
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extension]
        )
    icon = models.ImageField(
        upload_to='channel_icon_upload_path',
        blank=True,
        null=True,
        validators=[validate_icon_image_size, validate_image_file_extension]
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.id:
            # Check if the instance is being updated and  passing Category instance
            existing = get_object_or_404(Category, id=self.id)
            if existing.icon != self.icon:
                existing.icon.delete(save=False)
            if existing.banner != self.banner:
                existing.banner.delete(save=False)
        super(Category, self).save(*args, **kwargs)

    @receiver(models.signals.pre_delete, sender="server.Server")
    def category_delete_files(sender, instance, **kwargs):
        for field in instance._meta.fields:
            if field.name == 'icon':
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)

    def __str__(self):
        return self.name