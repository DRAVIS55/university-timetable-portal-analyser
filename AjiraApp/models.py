
from django.utils import timezone
from django.contrib.auth.models import User

# ------------------------
# Extra Displayer Models
# ------------------------

from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Confession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="confessions")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"


class Religion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    denomination = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='religion_files/', blank=True, null=True)  # new file field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Politics(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    party = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='politics_files/', blank=True, null=True)  # new file field
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Music(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='music_files/', blank=True, null=True)  # changed from audio_url
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.message[:20]}"


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"

# ------------------------
# Contact Messages
# ------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


# ------------------------
# Timetable
# ------------------------
class TimetableEntry(models.Model):
    course_code = models.CharField(max_length=20)        # e.g. COSC
    unit_code = models.CharField(max_length=50)          # e.g. "COSC 103(A)"
    unit_name = models.CharField(max_length=100, blank=True)
    year = models.IntegerField(null=True, blank=True)    # often unknown
    day = models.CharField(max_length=15)                # Monday..Friday
    time = models.CharField(max_length=50)               # exact slot label
    room = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["day", "time"]),
            models.Index(fields=["course_code"]),
            models.Index(fields=["room"]),
        ]

    def __str__(self):
        return f"{self.unit_code} - {self.day} {self.time} in {self.room}"


# ------------------------
# Advertisements
# ------------------------
class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# ------------------------
# News
# ------------------------
class News(models.Model):
    title = models.CharField(max_length=255)
    media = models.FileField(upload_to="news/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    @property
    def is_video(self):
        return self.media and self.media.url.lower().endswith(".mp4")


# ------------------------
# Reels
# ------------------------
class Reel(models.Model):
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="reels/")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# ------------------------
# Memos
# ------------------------
class Memo(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="memos/")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    @property
    def is_pdf(self):
        return self.file and self.file.url.lower().endswith(".pdf")


# ------------------------
# Hostels
# ------------------------
class Hostel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hostels/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


# ------------------------
# User Profiles
# ------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    passwordless = models.BooleanField(default=False)  # If true, skip login after first time

    def __str__(self):
        return self.user.username


