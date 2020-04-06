from uuid import uuid4
from functools import partial
from django.db.models import ImageField


class ImagePatternField(ImageField):
    context_instance_method = 'get_image_pattern_context'
    should_be_created_instance_method = 'image_pattern_should_be_created'

    def __init__(
            self,
            pattern,
            should_be_created=None,
            context=None,
            save_params=None,
            **kwargs
    ):
        self.pattern = pattern
        self.should_be_created_callback = should_be_created
        self.context = context
        self.save_params = save_params or {}
        kwargs['blank'] = True
        super().__init__(**kwargs)

    def pre_save(self, instance, add):
        file = getattr(instance, self.attname)

        if self.should_be_created(instance):
            file_name = self.get_file_name()
            context = self.get_context(instance)
            image = self.pattern(context=context).render_to_blob(**self.save_params)
            file.save(file_name, image, save=False)
        elif not file._committed:
            file.save(file.name, file.file, save=False)

        return file

    def should_be_created(self, instance):
        if self.should_be_created_callback:
            callback = self.should_be_created_callback
            method = partial(callback, instance)
        else:
            method = None

        method = method or getattr(instance, self.should_be_created_instance_method, None)
        return method() if method else True

    @staticmethod
    def get_file_name():
        return '{}.jpeg'.format(str(uuid4()))

    def get_context(self, instance):
        if self.context:
            callback = self.context
            method = partial(callback, instance)
        else:
            method = None

        method = method or getattr(instance, self.context_instance_method, None)
        return method() if method else True

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        kwargs.update({
            'pattern': self.pattern,
            'context': self.context,
            'should_be_created': self.should_be_created_callback,
            'save_params': self.save_params,
        })

        return name, path, args, kwargs
