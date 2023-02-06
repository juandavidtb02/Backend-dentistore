# Generated by Django 4.1.3 on 2023-02-06 06:44

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=20)),
                ('category_image', models.TextField()),
            ],
            options={
                'db_table': 'categories',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Colors',
            fields=[
                ('color_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('color_name', models.CharField(max_length=25)),
            ],
            options={
                'db_table': 'colors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Deliveries',
            fields=[
                ('delivery_id', models.AutoField(primary_key=True, serialize=False)),
                ('delivery_date', models.DateField()),
                ('delivery_price', models.IntegerField()),
                ('delivery_status', models.CharField(max_length=12)),
                ('delivery_descrip', models.CharField(blank=True, max_length=280, null=True)),
            ],
            options={
                'db_table': 'deliveries',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Images_products',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_name', models.CharField(max_length=30)),
                ('image_text', models.TextField()),
            ],
            options={
                'db_table': 'images_products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField()),
                ('order_status', models.CharField(max_length=12)),
                ('order_ammount', models.IntegerField()),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=30)),
                ('product_price', models.IntegerField()),
                ('product_stock', models.IntegerField()),
                ('product_image', models.CharField(blank=True, max_length=200, null=True)),
                ('product_descrip', models.CharField(blank=True, max_length=300, null=True)),
                ('product_details', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'db_table': 'products',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('size_id', models.AutoField(primary_key=True, serialize=False)),
                ('size_name', models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={
                'db_table': 'size',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'userlog',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Product_size',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.products')),
                ('size_stock', models.IntegerField()),
            ],
            options={
                'db_table': 'product_size',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.products')),
                ('color_stock', models.IntegerField()),
            ],
            options={
                'db_table': 'product_color',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.products')),
                ('sale_quantity', models.SmallIntegerField()),
                ('sale_price', models.IntegerField()),
            ],
            options={
                'db_table': 'sales',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('usermail', models.CharField(max_length=30, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password_user', models.CharField(max_length=256)),
                ('userphone', models.CharField(blank=True, max_length=12, null=True)),
                ('userrole', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
