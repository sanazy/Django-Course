from django.db import models


class Movie (models.Model):
    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    name = models.CharField('عنوان', max_length=100)
    director = models.CharField('کارگردان', max_length=50)
    year = models.IntegerField('سال تولید')
    length = models.IntegerField('مدت زمان')
    description = models.TextField('توضیحات')
    poster = models.ImageField('پوستر', upload_to='movie_posters/')

    def __str__(self):
        return self.name


class Cinema (models.Model):
    class Meta:
        verbose_name = 'سینما'
        verbose_name_plural = 'سینما'

    #cinema_code = models.IntegerField(primary_key=True)
    name = models.CharField('نام', max_length=50)
    city = models.CharField('شهر', max_length=30, default='Tehran')
    capacity = models.IntegerField('گنجایش')
    phone = models.CharField('تلفن', max_length=20, null=True)
    address = models.TextField('آدرس')
    image = models.ImageField('تصویر', upload_to='cinema_images/', null=True)

    def __str__(self):
        return self.name


class ShowTime (models.Model):
    class Meta:
        verbose_name = 'سانس'
        verbose_name_plural = 'سانس'

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name='فیلم')
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name='سینما')

    start_time = models.DateTimeField('زمان شروع نمایش')
    price = models.IntegerField('قیمت')
    salable_seats = models.IntegerField('صندلی های قابل فروش')
    free_seats = models.IntegerField('صندلی های خالی')

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6
    status_choices = (
        (SALE_NOT_STARTED, 'فروش آغاز نشده'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYED, 'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )
    status = models.IntegerField('وضعیت', choices=status_choices)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return '{} تومان'.format(self.price)

    def is_full(self):
        return self.free_seats == 0

    def open_sale(self):
        if self.status == ShowTime.SALE_NOT_STARTED:
            self.status = ShowTime.SALE_OPEN
            self.save()
        else:
            raise Exception('Sale has been started before')

    def close_sale(self):
        if self.status == ShowTime.SALE_OPEN:
            self.status = ShowTime.SALE_CLOSED
            self.save()
        else:
            raise Exception('Sale is not open')

    def expire_showtime(self, is_canceled=True):
        if self.status not in (Showtime.MOVIE_PLAYED, ShowTime.SHOW_CANCELED):
            self.status = ShowTime.SHOW_CANCELED if is_canceled else ShowTime.MOVIE_PLAYED
            self.save()
        else:
            raise Exception('Show has been expired before')

    def reserve_seats(self, seat_count):
        assert isinstance(seat_count, int) and seat_count > 0, 'Number of seats should'
        assert self.status == Showtime.SALE_OPEN, 'Sale is not open'
        assert self.free_seats >= seat_count, 'Not enough free seats'
        if self.free_seats == 0:
            self.status = ShowTime.TICKETS_SOLD
        self.save()


class Ticket(models.Model):
    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'

    showtime = models.ForeignKey('ShowTime', on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name='خریدار')
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید', auto_now_add=True)

    def __str__(self):
        return ' {} بلیت به نام {} برای فیلم {}'.format(self.seat_count, self.customer, self.showtime.movie)