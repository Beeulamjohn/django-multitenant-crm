from .models import Company


def get_user_company(user):

    try:

        return Company.objects.get(
            user=user
        )

    except Company.DoesNotExist:

        return None