from django.db.models import (
    Model,
    CharField,
)
from image_pattern.contrib.django import ImagePatternField

from .image_patterns import (
    ImagePattern,
    ImageContext,
)


class Statuses:
    DRAFT = 'draft'
    PUBLISH = 'publish'

    CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISH, 'Publish'),
    )


class ExampleModel(Model):
    text = CharField(
        max_length=200,
        verbose_name='Text for snippet image',
    )

    def get_image_pattern_context(self):
        return ImageContext(
            text=self.text,
        )

    def image_pattern_should_be_created(self):
        return self.status == Statuses.PUBLISH

    image_with_custom_methods = ImagePatternField(
        ImagePattern,
        verbose_name='Фотография',
        blank=True,
        null=True,
        context=get_image_pattern_context,
        should_be_created=image_pattern_should_be_created,
    )
    image = ImagePatternField(
        ImagePattern,
        verbose_name='Фотография',
        blank=True,
        null=True,
    )
    status = CharField(
        max_length=20,
        choices=Statuses.CHOICES,
    )

    class Meta:
        verbose_name = 'example object'
        verbose_name_plural = 'example objects'
