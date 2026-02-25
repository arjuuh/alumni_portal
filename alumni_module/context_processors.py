from .models import Connection

def follower_notifications(request):
    if request.user.is_authenticated:

        unread_followers = Connection.objects.filter(
            following=request.user,
            is_read=False
        ).select_related("follower")

        following_ids = request.user.following.values_list("following_id", flat=True)

        return {
            "notification_followers": unread_followers,
            "notification_following_ids": following_ids,
            "notification_count": unread_followers.count(),
        }

    return {}