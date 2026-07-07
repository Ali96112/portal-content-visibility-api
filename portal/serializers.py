from rest_framework import serializers

from .models import ContentItem


class ContentItemSerializer(serializers.ModelSerializer):
    allowed_groups = serializers.SerializerMethodField()

    class Meta:
        model = ContentItem
        fields = [
            "id",
            "title",
            "body",
            "content_type",
            "shared_with_all",
            "allowed_groups",
            "created_at",
        ]

    def get_allowed_groups(self, obj):
        return [
            {
                "id": audience.group.id,
                "name": audience.group.name,
            }
            for audience in obj.audience_groups.select_related("group").all()
        ]