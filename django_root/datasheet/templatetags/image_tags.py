from django import template
from django.core.exceptions import ObjectDoesNotExist

from wagtail.images.models import Image

register = template.Library()

# Display photo using id
@register.simple_tag
def image_url(image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except ObjectDoesNotExist:
        raise template.TemplateSyntaxError(
            "The image ID supplied is invalid"
        )
    return image.file.url
