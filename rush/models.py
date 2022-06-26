from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=40, blank=True)
    last_name = models.CharField(_("last name"), max_length=120, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    is_verified = models.BooleanField(default=False, null=False)
    picture = models.URLField(null=True, blank=True)
    banner = models.URLField(null=True, blank=True)
    birth_date = models.DateField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = (
        "first_name",
        "last_name",
        "email",
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class UserFriend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "friend",
        )


class Group(models.Model):
    name = models.CharField(max_length=240, null=False, blank=False)
    about = models.TextField()
    picture = models.URLField(blank=True, null=True)
    banner = models.URLField(blank=True, null=True)
    only_admin_post = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)


class GroupMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="member")
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "group",
        )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, related_name="group"
    )
    content = models.TextField(blank=False, null=False)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
