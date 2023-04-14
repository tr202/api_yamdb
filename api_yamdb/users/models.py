from django.contrib.auth.models import AbstractUser
from django.db import models


class RoleChoices(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class YamdbUser(AbstractUser):
    username = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        max_length=254
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        blank=False,
        default=RoleChoices.USER,
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_status_valid',
                check=models.Q(role__in=RoleChoices.values),
            ),
        )
        ordering = ('pk',)

    @property
    def is_admin(self):
        return self.is_superuser or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def is_owner(self, obj):
        return obj == self

    def __str__(self):
        return self.username
