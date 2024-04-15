from django.forms import EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.dispatch import receiver
from django.apps import AppConfig   
from django.db.models.signals import post_save



class UserCreationForm(UserCreationForm):
    email = EmailField(label=("Email address"), required=True, help_text=("Required."))
    is_superuser = models.BooleanField("IS SUPERUSER", default=False)
    remember_me = models.BooleanField(label=("Remember me"), required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2","is_superuser")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    


class Image(models.Model):
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='images/')
    ativo = models.BooleanField(default=True)


class CustomUser(AbstractUser):
    remember_me = models.BooleanField(default=False)
    custom_permissions = models.ManyToManyField(Permission, blank=True, related_name='home.CustomUser.user_permissions')

    class Meta:
        permissions = []

@receiver(post_save, sender=CustomUser)
def add_default_permissions(sender, instance, created, **kwargs):
    if created:
        instance.custom_permissions.add(*Permission.objects.filter(user=None))