# Generated migration to update field import paths from quantityfield to django_pint

from django.db import migrations

import django_pint.fields


class Migration(migrations.Migration):
    dependencies = [
        ("dummyapp", "0002_offsetunitfloatfieldsavemodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bigintfieldsavemodel",
            name="weight",
            field=django_pint.fields.BigIntegerQuantityField(
                base_units="gram", unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="choicesdefinedinmodel",
            name="weight",
            field=django_pint.fields.QuantityField(
                base_units="kilogram", unit_choices=["milligram", "pounds"]
            ),
        ),
        migrations.AlterField(
            model_name="choicesdefinedinmodelint",
            name="weight",
            field=django_pint.fields.IntegerQuantityField(
                base_units="kilogram", unit_choices=["milligram", "pounds"]
            ),
        ),
        migrations.AlterField(
            model_name="customuregdecimalhaybale",
            name="custom_decimal",
            field=django_pint.fields.DecimalQuantityField(
                base_units="custom",
                decimal_places=2,
                max_digits=10,
                unit_choices=["custom"],
            ),
        ),
        migrations.AlterField(
            model_name="customureghaybale",
            name="custom",
            field=django_pint.fields.QuantityField(
                base_units="custom", unit_choices=["custom"]
            ),
        ),
        migrations.AlterField(
            model_name="customureghaybale",
            name="custom_bigint",
            field=django_pint.fields.BigIntegerQuantityField(
                base_units="custom", unit_choices=["custom"]
            ),
        ),
        migrations.AlterField(
            model_name="customureghaybale",
            name="custom_int",
            field=django_pint.fields.IntegerQuantityField(
                base_units="custom", unit_choices=["custom"]
            ),
        ),
        migrations.AlterField(
            model_name="decimalfieldsavemodel",
            name="weight",
            field=django_pint.fields.DecimalQuantityField(
                base_units="gram",
                decimal_places=2,
                max_digits=10,
                unit_choices=["gram"],
            ),
        ),
        migrations.AlterField(
            model_name="emptyhaybalebigint",
            name="weight",
            field=django_pint.fields.BigIntegerQuantityField(
                base_units="gram", null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="emptyhaybaledecimal",
            name="weight",
            field=django_pint.fields.DecimalQuantityField(
                base_units="gram",
                decimal_places=2,
                max_digits=10,
                null=True,
                unit_choices=["gram"],
            ),
        ),
        migrations.AlterField(
            model_name="emptyhaybalefloat",
            name="weight",
            field=django_pint.fields.QuantityField(
                base_units="gram", null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="emptyhaybaleint",
            name="weight",
            field=django_pint.fields.IntegerQuantityField(
                base_units="gram", null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="emptyhaybalepositiveint",
            name="weight",
            field=django_pint.fields.PositiveIntegerQuantityField(
                base_units="gram", null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="floatfieldsavemodel",
            name="weight",
            field=django_pint.fields.QuantityField(
                base_units="gram", unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="haybale",
            name="weight",
            field=django_pint.fields.QuantityField(
                base_units="gram", unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="haybale",
            name="weight_bigint",
            field=django_pint.fields.BigIntegerQuantityField(
                base_units="gram", blank=True, null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="haybale",
            name="weight_int",
            field=django_pint.fields.IntegerQuantityField(
                base_units="gram", blank=True, null=True, unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="intfieldsavemodel",
            name="weight",
            field=django_pint.fields.IntegerQuantityField(
                base_units="gram", unit_choices=["gram"]
            ),
        ),
        migrations.AlterField(
            model_name="offsetunitfloatfieldsavemodel",
            name="weight",
            field=django_pint.fields.QuantityField(
                base_units="degC", unit_choices=["degC"]
            ),
        ),
    ]
