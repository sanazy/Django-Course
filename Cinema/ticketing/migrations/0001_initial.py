# Generated by Django 3.0.3 on 2020-03-13 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام')),
                ('city', models.CharField(default='Tehran', max_length=30, verbose_name='شهر')),
                ('capacity', models.IntegerField(verbose_name='گنجایش')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='تلفن')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('image', models.ImageField(null=True, upload_to='cinema_images/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'سینما',
                'verbose_name_plural': 'سینما',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
                ('director', models.CharField(max_length=50, verbose_name='کارگردان')),
                ('year', models.IntegerField(verbose_name='سال تولید')),
                ('length', models.IntegerField(verbose_name='مدت زمان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('poster', models.ImageField(upload_to='movie_posters/', verbose_name='پوستر')),
            ],
            options={
                'verbose_name': 'فیلم',
                'verbose_name_plural': 'فیلم',
            },
        ),
        migrations.CreateModel(
            name='ShowTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='زمان شروع نمایش')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('salable_seats', models.IntegerField(verbose_name='صندلی های قابل فروش')),
                ('free_seats', models.IntegerField(verbose_name='صندلی های خالی')),
                ('status', models.IntegerField(choices=[(1, 'فروش آغاز نشده'), (2, 'در حال فروش بلیت'), (3, 'بلیت ها تمام شد'), (4, 'فروش بلیت بسته شد'), (5, 'فیلم پخش شد'), (6, 'سانس لغو شد')], verbose_name='وضعیت')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.Cinema', verbose_name='سینما')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.Movie', verbose_name='فیلم')),
            ],
            options={
                'verbose_name': 'سانس',
                'verbose_name_plural': 'سانس',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_count', models.IntegerField(verbose_name='تعداد صندلی')),
                ('order_time', models.DateTimeField(auto_now_add=True, verbose_name='زمان خرید')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.Profile', verbose_name='خریدار')),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.ShowTime', verbose_name='سانس')),
            ],
            options={
                'verbose_name': 'بلیت',
                'verbose_name_plural': 'بلیت',
            },
        ),
    ]
