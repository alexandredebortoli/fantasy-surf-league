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


class PredictionManager(models.Manager):
    def total_points_for_user(self, user):
        return self.filter(user=user).aggregate(total_points=models.Sum("points"))[
            "total_points"
        ]

    def total_correct_predictions_for_user(self, user):
        static_predictions = self.filter(user=user, event__status="Completed")
        count = 0
        for static_prediction in static_predictions:
            if static_prediction.first == static_prediction.event.first_place:
                count += 1
            if static_prediction.second == static_prediction.event.second_place:
                count += 1
        return count

    def total_incorrect_predictions_for_user(self, user):
        static_predictions = self.filter(user=user, event__status="Completed")
        count = 0
        for static_prediction in static_predictions:
            if static_prediction.first != static_prediction.event.first_place:
                count += 1
            if static_prediction.second != static_prediction.event.second_place:
                count += 1
        return count


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    event = models.ForeignKey(
        "Event", on_delete=models.CASCADE, related_name="predictions"
    )
    first = models.ForeignKey(
        "Surfer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="predictions_first",
    )
    second = models.ForeignKey(
        "Surfer",
        on_delete=models.SET_NULL,
        null=True,
        related_name="predictions_second",
    )
    points = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PredictionManager()

    def __str__(self):
        return f"{self.user.username} - event #{self.event.number}"


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


class Surfer(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    headshot_url = models.URLField(max_length=200, null=False)
    country = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Event(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=False,
    )
    status = models.CharField(max_length=100, null=False)
    first_place = models.ForeignKey(
        Surfer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="first_place",
    )
    second_place = models.ForeignKey(
        Surfer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="second_place",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Event #{self.number}: {self.name} - {self.location}"


class Ranking(models.Model):
    surfer = models.ForeignKey(
        Surfer, on_delete=models.CASCADE, related_name="rankings"
    )
    rank = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=False,
    )
    points = models.CharField(max_length=7, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.surfer.name} - Rank #{self.rank}"
