from secrets import choice
from tokenize import group
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    GENDERS = (
        ('Male', 'Masculino'),
        ('Female', 'Feminino'),
        ('Undefined', None)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=120, choices=GENDERS, null=True)
    is_verified = models.BooleanField(default=False)
    birth_date = models.DateField()
    email = models.EmailField()
    picture = models.URLField()
    banner = models.URLField()


class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class Group(models.Model):
    name = models.CharField(max_length=240, null=False, blank=False)
    about = models.TextField()
    picture = models.URLField()
    banner = models.URLField()
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class GroupConfig(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='config')
    only_admin_post = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)


class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='member')
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    content = models.TextField(blank=False, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class UserReaction(models.Model):
    REACTIONS = (
        ('LIKE', 'LIKE'),
        ('LAUGH', 'LAUGH'),
        ('LOVED', 'LOVED'),
        ('CRY', 'CRY'),
        ('SAD', 'SAD'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reaction')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reaction')
    type = models.CharField(max_length=120, choices=REACTIONS, blank=False, null=False)
