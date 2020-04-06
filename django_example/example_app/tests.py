from os import remove
from django.test import TestCase
from image_pattern import __version__

from .models import (
    ExampleModel,
    Statuses,
)


class ImagePatternTestCase(TestCase):
    text = 'What time is it?'

    def test_version(self):
        self.assertEqual(__version__, '0.0.18')

    def test_image_create(self):
        instance: ExampleModel = ExampleModel(text=self.text)
        instance.status = Statuses.DRAFT

        instance.save()

        self.assertIsNone(instance.image.name)
        self.assertIsNone(instance.image_with_custom_methods.name)

        instance.status = Statuses.PUBLISH
        instance.save()

        self.assertIsNotNone(instance.image.name)
        self.assertIsNotNone(instance.image_with_custom_methods.name)

    def tearDown(self) -> None:
        for instance in ExampleModel.objects.all():
            instance.image.storage.delete(instance.image.name)
            instance.image_with_custom_methods.storage.delete(instance.image_with_custom_methods.name)
