# Generated by Django 4.2.6 on 2024-04-17 01:35

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCadastrados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_user', models.CharField(max_length=30)),
                ('imagem_vinculada_user', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, null=True, quality=100, scale=None, size=[480, 480], upload_to='media/')),
            ],
        ),
    ]