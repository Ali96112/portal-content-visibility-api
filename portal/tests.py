from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ContentAudienceGroup, ContentItem, InvestorGroup, Membership


class ContentVisibilityTests(APITestCase):
    def setUp(self):
        self.ali = User.objects.create_user(
            username="ali",
            email="ali@example.com",
            password="password123"
        )

        self.sara = User.objects.create_user(
            username="sara",
            email="sara@example.com",
            password="password123"
        )

        self.series_a = InvestorGroup.objects.create(name="Series A")
        self.board_observers = InvestorGroup.objects.create(name="Board Observers")

        Membership.objects.create(
            user=self.ali,
            group=self.series_a
        )

        self.public_content = ContentItem.objects.create(
            title="General Company Announcement",
            body="This announcement is visible to all shareholders.",
            content_type=ContentItem.ANNOUNCEMENT,
            shared_with_all=True
        )

        self.series_a_content = ContentItem.objects.create(
            title="Series A Financial Report",
            body="This report is only for Series A shareholders.",
            content_type=ContentItem.DOCUMENT,
            shared_with_all=False
        )

        ContentAudienceGroup.objects.create(
            content=self.series_a_content,
            group=self.series_a
        )

        self.board_content = ContentItem.objects.create(
            title="Board Observer Notes",
            body="This content is only for Board Observers.",
            content_type=ContentItem.DOCUMENT,
            shared_with_all=False
        )

        ContentAudienceGroup.objects.create(
            content=self.board_content,
            group=self.board_observers
        )

    def test_user_can_view_content_shared_with_all(self):
        response = self.client.get(
            f"/api/contents/{self.public_content.id}/?user_id={self.ali.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "General Company Announcement")

    def test_user_can_view_restricted_content_if_member_of_allowed_group(self):
        response = self.client.get(
            f"/api/contents/{self.series_a_content.id}/?user_id={self.ali.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Series A Financial Report")

    def test_user_cannot_view_restricted_content_if_not_member_of_allowed_group(self):
        response = self.client.get(
            f"/api/contents/{self.board_content.id}/?user_id={self.ali.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)