# Generated by Django 2.2.6 on 2019-11-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='expire',
            field=models.IntegerField(default=0, verbose_name='有效期周期'),
        ),
    ]
