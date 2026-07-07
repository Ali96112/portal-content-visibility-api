from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ContentItem, Membership
from .serializers import ContentItemSerializer


def get_fake_authenticated_user(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        raise ValidationError({"user_id": "This query parameter is required."})

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError({"user_id": "Invalid user_id."})


def get_visible_content_for_user(user):
    user_group_ids = Membership.objects.filter(user=user).values_list(
        "group_id",
        flat=True
    )

    return (
        ContentItem.objects.filter(
            Q(shared_with_all=True)
            | Q(shared_with_all=False, audience_groups__group_id__in=user_group_ids)
        )
        .distinct()
        .order_by("-created_at")
    )


class ContentListView(APIView):
    def get(self, request):
        user = get_fake_authenticated_user(request)

        try:
            limit = int(request.query_params.get("limit", 10))
            offset = int(request.query_params.get("offset", 0))
        except ValueError:
            return Response(
                {"detail": "limit and offset must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if limit <= 0 or offset < 0:
            return Response(
                {"detail": "limit must be positive and offset cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = get_visible_content_for_user(user)
        total_count = queryset.count()

        paginated_queryset = queryset[offset: offset + limit]

        serializer = ContentItemSerializer(paginated_queryset, many=True)

        return Response(
            {
                "count": total_count,
                "limit": limit,
                "offset": offset,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ContentDetailView(APIView):
    def get(self, request, pk):
        user = get_fake_authenticated_user(request)

        try:
            content = ContentItem.objects.get(pk=pk)
        except ContentItem.DoesNotExist:
            return Response(
                {"detail": "Content not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_visible = get_visible_content_for_user(user).filter(id=content.id).exists()

        if not is_visible:
            return Response(
                {"detail": "You do not have permission to view this content."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ContentItemSerializer(content)

        return Response(serializer.data, status=status.HTTP_200_OK)
