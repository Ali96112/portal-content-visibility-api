from django.contrib.auth.models import User
from django.db import models


class InvestorGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    group = models.ForeignKey(
        InvestorGroup,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"


class ContentItem(models.Model):
    ANNOUNCEMENT = "announcement"
    DOCUMENT = "document"

    CONTENT_TYPES = [
        (ANNOUNCEMENT, "Announcement"),
        (DOCUMENT, "Document"),
    ]

    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)

    # If True, all shareholders can see this content.
    # If False, only selected groups can see it.
    shared_with_all = models.BooleanField(default=True)

    allowed_groups = models.ManyToManyField(
        InvestorGroup,
        through="ContentAudienceGroup",
        related_name="content_items",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ContentAudienceGroup(models.Model):
    content = models.ForeignKey(
        ContentItem,
        on_delete=models.CASCADE,
        related_name="audience_groups"
    )
    group = models.ForeignKey(
        InvestorGroup,
        on_delete=models.CASCADE,
        related_name="content_audiences"
    )

    class Meta:
        unique_together = ("content", "group")

    def __str__(self):
        return f"{self.content.title} -> {self.group.name}"
