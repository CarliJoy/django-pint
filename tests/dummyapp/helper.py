from django.db.models.base import ModelBase

from quantityfield.fields import QuantityFieldMixin

from .models import *  # noqa: F401, F403


def get_test_models() -> dict[str, ModelBase]:
    """
    Get a list of all Test models
    """
    result = {}
    for name, obj in globals().items():
        if (
            not name.startswith("_")
            and isinstance(obj, ModelBase)
            and not obj._meta.abstract
            and obj._meta.app_config.name.endswith("dummyapp")
        ):
            result[name] = obj
    return result


def print_admins():
    for model in sorted(get_test_models().keys()):
        print(f"admin.site.register({model}, ReadOnlyEditing)")


def print_test_admin_choices():
    for model_name, model in get_test_models().items():
        for field in model._meta.fields:
            if isinstance(field, QuantityFieldMixin):
                print(f"(models.{model_name}, '{field.name}'),")
