# Generated by Django 2.0 on 2017-12-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='姓名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], default='男', max_length=32, verbose_name='性别')),
                ('c_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'ordering': ['-c_time'],
            },
        ),
    ]