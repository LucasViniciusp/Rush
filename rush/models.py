from secrets import choice
from tokenize import group
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    GENDER_UNDEFINED = 0
    GENDER_FEMALE = 1
    GENDER_MALE = 2

    GENDERS = (
        (GENDER_UNDEFINED, 'Undefined'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_MALE, 'Male'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.IntegerField(choices=GENDERS, default=GENDER_UNDEFINED)
    is_verified = models.BooleanField(default=False, null=False)
    birth_date = models.DateField(null=True)
    email = models.EmailField(null=False, blank=False)
    picture = models.URLField(null=True, blank=True)
    banner = models.URLField(null=True, blank=True)


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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, related_name='group')
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
