from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from PIL import Image


# Create your models here.
class User(AbstractUser):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=48, choices=GENDER)
    date_of_birth = models.DateField(null=False)
    profile_picture = models.ImageField(upload_to="profile_pictures/uploaded_by_users/", blank=True, null=True,
                                        default="profile_pictures/default_avatar.png")
    created_at = models.DateTimeField("date created", default=timezone.now)
    REQUIRED_FIELDS = ["email", "date_of_birth"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)
