# Generated by Django 3.1.2 on 2020-11-09 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20201109_2350'),
        ('medical', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='location.locality')),
                ('medical_helper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='medical.medicalhelper')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='account.user')),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='beneficiary.parent')),
            ],
        ),
    ]
