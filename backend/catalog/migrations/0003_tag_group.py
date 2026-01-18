from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_category_tag_product_is_visible_variant_old_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="group",
            field=models.CharField(blank=True, default="", max_length=80),
        ),
    ]