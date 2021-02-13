from django.core.exceptions import ObjectDoesNotExist


class DBUtils:
    def get_or_none(self, model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None