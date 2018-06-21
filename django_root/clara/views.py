import requests
import base64

from django.conf import settings
from django.http.response import StreamingHttpResponse

from rest_framework.views import APIView


class ClaraView(APIView):
    """
    Clara download view
    """
    def download(self, uuid=None):
        url = settings.CLARA_EXPORT_ENDPOINT
        user = settings.CLARA_USERNAME
        token = settings.CLARA_API_TOKEN

        auth = base64.encodestring(
            ("{user}:{api_token}".format(user=user, api_token=token)).encode('ascii')
        ).decode('ascii').replace('\n', '')

        request = requests.get(
            url.format(uuid=uuid),
            headers={'Authorization': 'Basic %s' % auth},
            stream=True
        )

        response = StreamingHttpResponse(request.iter_content(), content_type="application/zip")
        # response['Content-Disposition'] = 'attachment; filename="3d-model.zip"'
        return response
