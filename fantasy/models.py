import random
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)
    league = models.ForeignKey(
        "League",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    event_identifier = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False,
    )
    first_name = models.CharField(max_length=100, null=False)
    second_name = models.CharField(max_length=100, null=False)
    is_first_correct = models.BooleanField(default=False)
    is_second_correct = models.BooleanField(default=False)
    points = models.IntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - event #{self.event_identifier}"


class League(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(
        User, related_name="league_created", on_delete=models.CASCADE
    )
    identifier = models.CharField(
        max_length=12, null=False, unique=True, editable=False, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Join #{self.identifier}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_identifier()
        super().save(*args, **kwargs)

    def generate_identifier(self):
        league_uuid = str(uuid.uuid4())
        random_chars = "".join(random.sample(league_uuid.replace("-", ""), 9))
        self.identifier = "-".join(
            [random_chars[:3], random_chars[3:6], random_chars[6:]]
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.generate_identifier()
        super().save(*args, **kwargs)
