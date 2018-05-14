

from teconn.blocks import CarouselImageBlock



class PanasonicCarouselImageBlock(CarouselImageBlock):
    class Meta:
        template = 'panasonic/blocks/_carousel_image.html'
