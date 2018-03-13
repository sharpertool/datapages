import requests

from wagtail.embeds.exceptions import EmbedException, EmbedNotFoundException

from wagtail.embeds.finders.base import EmbedFinder


class IFramelyException(EmbedException):
    pass


class AccessDeniedIFramelyException(IFramelyException):
    pass


class IFramely:
    """ Wrap oEmbed prototcol here """
    api_url = 'https://iframe.ly/api/oembed'
    keylist = ['title', 'author_name',
               'provider_name', 'type',
               'thumbnail_url', 'thumbnail_height', 'thumbnail_width',
               'width', 'height', 'html', 'version']

    def __init__(self, key=None):
        self.key = key
        print("Initialize IFramely finder")

    def oembed(self, url='', maxwidth=640, better=False):
        url_params = {
            'api_key' : self.key,
            'url': url
        }
        r = requests.get(self.api_url, params=url_params,
                         timeout=1.0)

        res = {
            'error': r.status_code != 200,
            'error_code': r.status_code,
            'error_text': r.reason,
        }

        if (r.status_code == 200):
            rfiltered = {k: v for k, v in r.json().items() if k in self.keylist}
            res.update(rfiltered)

        return res


class IFramelyFinder(EmbedFinder):
    key = None

    def __init__(self, key=None):
        if key:
            self.key = key

    def get_key(self):
        return self.key

    def accept(self, url):
        # We don't really know what embedly supports so accept everything
        return True

    def find_embed(self, url, max_width=None, key=None):

        print("Searching IFrame.ly for url {}".format(url))
        # Get embedly key
        if key is None:
            key = self.get_key()

        # Get embedly client
        client = IFramely(key=key)

        # Call embedly
        if max_width is not None:
            oembed = client.oembed(url, maxwidth=max_width, better=False)
        else:
            oembed = client.oembed(url, better=False)

        # Check for error
        if oembed.get('error'):
            if oembed['error_code'] in [401, 403]:
                raise AccessDeniedIFramelyException
            elif oembed['error_code'] == 404:
                raise EmbedNotFoundException
            else:
                raise IFramelyException

        # Convert photos into HTML
        if oembed['type'] == 'photo':
            html = '<img src="%s" />' % (oembed['url'], )
        else:
            html = oembed.get('html')

        # Return embed as a dict
        return {
            'title': oembed['title'] if 'title' in oembed else '',
            'author_name': oembed['author_name'] if 'author_name' in oembed else '',
            'provider_name': oembed['provider_name'] if 'provider_name' in oembed else '',
            'type': oembed['type'],
            'thumbnail_url': oembed.get('thumbnail_url'),
            'width': oembed.get('width'),
            'height': oembed.get('height'),
            'html': html,
        }


embed_finder_class = IFramelyFinder
