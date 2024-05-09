from django.db import models
import datetime
# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


class Cinema(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='uploads/cinema/')
    location = models.CharField(max_length=60)
    phone = PhoneNumberField(null=False, blank=True, unique=False)
    email = models.EmailField(max_length = 254)

    @staticmethod
    def get_all_cinemas():
        return Cinema.objects.all()

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=60)
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Film(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to='uploads/film/', default='default.jpg')
    description = models.CharField(max_length=400, default='')
    genres = models.CharField(max_length=50, default='')
    countries = models.CharField(max_length=400, default='')
    duration = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.name

class Session(models.Model):
    date = models.DateField(default=datetime.datetime.today())
    time = models.TimeField(default=datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    film_id = models.ForeignKey(Film, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)], default=50)

    def __str__(self):
        return f"{self.film_id.name} - {self.hall_id} - {self.date} {self.time} - {self.price}"

    @staticmethod
    def get_all_sessions():
        return Session.objects.all()

    @staticmethod
    def get_all_session_by_date(date):
        if date:
            return Session.objects.filter(date=date)
        else:
            return Session.get_all_sessions()

class Ticket(models.Model):
  session = models.ForeignKey(Session, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0)], default=50)
  is_available = models.BooleanField(default=True)
  seat_number = models.IntegerField()  # Field for seat number
  row_number = models.CharField(max_length=10)  # Field for row number (adjust max_length as needed)