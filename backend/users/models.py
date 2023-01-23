from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import F, Q, UniqueConstraint

LENGTH_OF_USER_FIELDS = 50


class User(AbstractUser):
    """
    User model.
    """
    first_name = models.CharField(
        verbose_name='first name', max_length=LENGTH_OF_USER_FIELDS
    )
    last_name = models.CharField(
        max_length=LENGTH_OF_USER_FIELDS, verbose_name='last name',
    )
    email = models.EmailField(
        max_length=LENGTH_OF_USER_FIELDS, verbose_name='email',
        unique=True
    )
    username = models.CharField(
        verbose_name='username', max_length=LENGTH_OF_USER_FIELDS,
        unique=True, validators=(UnicodeUsernameValidator(),)
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return str(self.username)


class Follow(models.Model):
    """
    Model of following on authors.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Author',
        related_name='follower',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Follower',
        related_name='following'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='no_self_follow'
            )
        ]
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self) -> str:
        return f"{self.user} is following {self.author}"
