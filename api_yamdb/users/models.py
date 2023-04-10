from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class YamdbUserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        return self.create(email, password=None, **extra_fields)

    def create(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create(email, password, **extra_fields)


class RoleChoices(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class YamdbUser(AbstractUser):
    username = models.CharField(
        unique=True, blank=False, null=False, max_length=150)
    email = models.EmailField(
        unique=True, blank=False, null=False, max_length=254)
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

    objects = YamdbUserManager()

    class Meta:
        constraints = (
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(role__in=RoleChoices.values),
            ),
        )
        ordering = ('pk',)
