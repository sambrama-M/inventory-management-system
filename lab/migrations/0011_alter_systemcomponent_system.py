# Generated by Django 4.2 on 2024-07-30 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0010_itemremovalrecord_delete_itemrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemcomponent',
            name='system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lab.system'),
        ),
    ]