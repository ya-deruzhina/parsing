# Generated by Django 4.1 on 2024-10-15 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wb', '0002_remove_productmodel_count_remove_productmodel_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='brand_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='color',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='contents',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='name_product',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='options',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='price_without_nds',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='root_type_product',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='type_product',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='vendor_code',
            field=models.CharField(max_length=20),
        ),
    ]
