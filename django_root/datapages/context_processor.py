from django.conf import settings


def datapages_context(request):
    return {
        'clara_username': settings.CLARA_USERNAME,
        'clara_api_token': settings.CLARA_API_TOKEN
    }