# Generated by Django 5.1.7 on 2025-03-14 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
                ('full_name', models.CharField(max_length=150, verbose_name='Полное имя')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'ordering': ['email', 'full_name'],
            },
        ),
    ]
