# Generated by Django 2.1.7 on 2019-03-21 07:31

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthdate', models.DateField()),
            ],
            options={
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Capsule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=250)),
                ('emails', models.CharField(blank=True, max_length=2500)),
                ('capsule_type', models.CharField(choices=[('F', 'FREE'), ('P', 'PREMIUM'), ('M', 'MODULAR')], max_length=1)),
                ('private', models.BooleanField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('dead_man_switch', models.BooleanField()),
                ('dead_man_counter', models.BigIntegerField()),
                ('twitter', models.BooleanField()),
                ('facebook', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Credit_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holder_name', models.CharField(max_length=50)),
                ('brand_name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=24)),
                ('expiration_month', models.IntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('expiration_year', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(2019)])),
                ('cvv', models.IntegerField(validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('size', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('type', models.CharField(choices=[('F', 'FILE'), ('I', 'IMAGE')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('release_date', models.DateTimeField()),
                ('capsule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='main.Capsule')),
            ],
        ),
        migrations.CreateModel(
            name='Social_network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_type', models.CharField(choices=[('F', 'FACEBOOK'), ('T', 'TWITTER')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthdate', models.DateField()),
                ('email_notification', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='social_network',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to='main.User'),
        ),
        migrations.AddField(
            model_name='file',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='main.Module'),
        ),
        migrations.AddField(
            model_name='capsule',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capsuls', to='main.User'),
        ),
        migrations.AddField(
            model_name='capsule',
            name='credit_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capsuls', to='main.Credit_card'),
        ),
    ]