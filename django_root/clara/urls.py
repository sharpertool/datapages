from django.conf.urls import url

from .views import ClaraView

urlpatterns = [
    url(r'^download/(?P<uuid>([-0-9a-z]+))/$', ClaraView.download, name="download")
]