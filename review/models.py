from django.db.models import (
    Model, SmallIntegerField, CharField, TextField, GenericIPAddressField, DateTimeField, ForeignKey, CASCADE
)
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(Model):
    reviewer = ForeignKey(User, related_name="reviews", on_delete=CASCADE)
    company_name = CharField(max_length=255, db_index=True, help_text="Name of the reviewed company.")
    rating = SmallIntegerField(db_index=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                               help_text="Rating of the review.")
    title = CharField(max_length=64, db_index=True, help_text="Title of the review, keep it short.")
    summary = TextField(max_length=10000, help_text="Summary of the review.")
    ip_address = GenericIPAddressField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"{self.rating} - {self.title} - {self.company_name} - {self.reviewer.username}"
