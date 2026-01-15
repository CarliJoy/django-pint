from django.contrib import admin

from . import models


class ReadOnlyEditing(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return list(self.get_fields(request))
        return []


admin.site.register(models.BigIntFieldSaveModel, ReadOnlyEditing)
admin.site.register(models.ChoicesDefinedInModel, ReadOnlyEditing)
admin.site.register(models.ChoicesDefinedInModelInt, ReadOnlyEditing)
admin.site.register(models.CustomUregDecimalHayBale, ReadOnlyEditing)
admin.site.register(models.CustomUregHayBale, ReadOnlyEditing)
admin.site.register(models.DecimalFieldSaveModel, ReadOnlyEditing)
admin.site.register(models.EmptyHayBaleBigInt, ReadOnlyEditing)
admin.site.register(models.EmptyHayBaleDecimal, ReadOnlyEditing)
admin.site.register(models.EmptyHayBaleFloat, ReadOnlyEditing)
admin.site.register(models.EmptyHayBaleInt, ReadOnlyEditing)
admin.site.register(models.FloatFieldSaveModel, ReadOnlyEditing)
admin.site.register(models.HayBale, ReadOnlyEditing)
admin.site.register(models.IntFieldSaveModel, ReadOnlyEditing)
admin.site.register(models.OffsetUnitFloatFieldSaveModel, ReadOnlyEditing)
