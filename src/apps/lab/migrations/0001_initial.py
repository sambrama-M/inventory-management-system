# Generated by Django 4.2 on 2024-08-13 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_initial'),
        ('org', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=5, unique=True)),
                ('item_name', models.CharField(max_length=255)),
                ('total_qty', models.IntegerField(default=1)),
                ('in_use_qty', models.IntegerField(default=0)),
                ('total_available_qty', models.IntegerField(default=0)),
                ('removed_qty', models.IntegerField(default=0)),
                ('unit_of_measure', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.category')),
            ],
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab_name', models.CharField(max_length=255)),
                ('room_no', models.IntegerField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.department')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='org.org')),
                ('user', models.ManyToManyField(related_name='labs', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_code', models.CharField(max_length=5, unique=True)),
                ('sys_name', models.CharField(max_length=255, verbose_name='System Name')),
                ('status', models.CharField(choices=[('working', 'Working'), ('not_working', 'Not working'), ('item_missing', 'Item missing')], max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
            ],
        ),
        migrations.CreateModel(
            name='SystemComponent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(max_length=255)),
                ('component_type', models.CharField(choices=[('Mouse', 'Mouse'), ('Keyboard', 'Keyboard'), ('Processor', 'Processor'), ('RAM', 'RAM'), ('Storage', 'Storage'), ('OS', 'OS'), ('Monitor', 'Monitor'), ('CPU Cabin', 'CPU Cabin')], max_length=255)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.item')),
                ('system', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='lab.system')),
            ],
        ),
        migrations.CreateModel(
            name='LabSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items_tab', models.BooleanField(default=False)),
                ('sys_tab', models.BooleanField(default=False)),
                ('categories_tab', models.BooleanField(default=False)),
                ('brands_tab', models.BooleanField(default=False)),
                ('lab', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='lab.lab')),
            ],
        ),
        migrations.CreateModel(
            name='ItemRemovalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('Depreciation', 'Depreciation'), ('Consumption', 'Consumption')], max_length=255)),
                ('qty', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('remarks', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.item')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab'),
        ),
        migrations.AddField(
            model_name='category',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab'),
        ),
        migrations.AddField(
            model_name='brand',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lab.lab'),
        ),
    ]