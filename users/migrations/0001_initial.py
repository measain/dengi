# Generated by Django 4.0.4 on 2022-05-28 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=32)),
                ('first_name', models.CharField(blank=True, max_length=64, verbose_name='Имя')),
                ('awaitable_action', models.CharField(blank=True, choices=[('new_lifer', 'Свежий кабанчик (с)'), ('set_sum', 'Указание суммы'), ('set_deadline', 'Указание срока'), ('default', 'Запись трат')], max_length=32, verbose_name='Текущее действие')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
